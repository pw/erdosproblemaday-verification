VERDICT: HOLDS AS READ. Nothing fatal and no gap. Every step (i) through (vii) was re-derived in full. The objections below are MINOR or NOTE only.

Referee seat A (hostile), 2026-10-13. Target: Didin & Pimenov, "An Asymptotic Solution to the (1:2)-Biased Erdős Clique-Building Game", zenodo 21813052, `clique12_en_v3.pdf`, read in both the PDF render and the text layer. Table entries were checked against the rendered page. The Bella column for P_U reads 6/5, not 5/6; the text layer garbles this. The RU v3 constants match the EN version. I did not read the Lean files or other seats.

## Objections

**1. NOTE (scope and size of "sufficiently large").** The paper says: "We prove the 1 : 2 case for all sufficiently large n." Problem #778, as live on erdosproblems.com 2026-10-13, asks "does Bob have a winning strategy for n>3?" The paper resolves it only for large n, and says so. Quantitatively, η = −log θ = 0.0097123, so C > 2/η = 205.924. Using the paper's own displayed bounds, the first integer log n at which both Φ_init < 1 and R(n) ≥ a hold is log n = 156 (C = 206: a = 286, ℓ = 32136, R = 286), which is n ≳ 10^67.7. The binding constraint is the clique comparison R(n) > a − 1. The Φ_init bound is about 1.8e−68 there. This is honest asymptotics, but it says nothing about any n that could be checked by computer.

**2. MINOR (citation understates prior work).** The paper says: "Malekshahian and Spiro proved the corresponding asymptotic result for bias 1 : 4 [2], and Cambie and Provoost for bias 1 : 3 [3]."
- Cambie–Provoost v2 (arXiv:2505.03497v2, 28 Oct 2025), Theorem 8: "For every n ≥ 4, Clique^(1,3)(n) is won by player 2." This is proved in Theorems 18 (n even) and 19 (n odd). It is an every-n result, not an "asymptotic" one.
- CP v2 Conjecture 17 asks for exactly the large-n (p, p+1) statement, and the present theorem is its p = 1 case. The paper should cite that conjecture.

**3. NOTE (Malekshahian–Spiro citation is CORRECT as cited).**
- arXiv:2410.18304v2 (5 May 2026), Theorem 3: Player 2 wins Clique^(p,q)(n) for n ≥ n0 when q ≥ (2 + 12 log2 log2(p+1)/log2(p+1))·p + 2. With p = 1 this gives q ≥ 4, and the paper states verbatim: "In particular, for all sufficiently large n, the game Clique(1,4)(n) is a Player 2 win."
- The "15:1/14:1" figure in the live-page comment is v1. MS v2's own intro says "the original version of this paper gave … q = 15", and CP v2 says "in [11], it is proved with q = 15".
- MS's biased-game definition matches the paper's game exactly: Player 1 first with p edges, last-turn remainder convention, and for p < q Player 2 wins iff strictly larger. This is also problem #778 ("Bob colours two edges after each edge that Alice colours … strictly larger").
- Chronology nit: CP's 1:3 result (2025) predates MS v2's 1:4 result (2026). The sentence order could suggest the reverse.

**4. NOTE.** The paper says: "Lemma 1. After Bella's opening move, Φ does not increase during any round." Read literally, this is false within a round, because Bella's move adds exactly 2d\*(z) ≥ 0. What is proved, and what is used, is that Φ does not increase net across each round C,C,B, and does not increase across a terminal Chingiz turn. Harmless.

**5. NOTE (part of question 4).** The paper says: "All weights below are initialized immediately after Bella's opening move." Q_A and P_U are functions of the position, so nothing is actually initialized. The sentence only fixes t = 0 for tracking Φ. This is consistent with Lemma 1:
- Round 1 is C,C,B, played after the opening.
- The opening edge's effect is absorbed into the factor 3 in the Q-sum bound and the factor 6/5 in the P-sum bound. Before the opening, Q_A = 3^−h and P_U = (4/3)^{3H/5}(5/6)^H = θ^H. One Bella edge multiplies each weight by at most 3 or 6/5 respectively.

No accounting gap.

**6. NOTE.** The paper says: "Chingiz claims two, or all remaining edges if fewer than two remain." … "If the game ends on Chingiz's turn, Φ only decreases."
- The fewer-than-two clause can never trigger. C(n,2) mod 3 is always 0 or 1, so C(n,2) − 1 after the opening is ≡ 2 or 0 (mod 3).
- The game therefore ends either after a full two-edge Chingiz turn (n ≡ 0, 1 mod 3) or after a Bella move (n ≡ 2 mod 3).
- The truncated case is handled correctly, because Chingiz moves only decrease Φ.

**7. NOTE (proof order in Lemma 2).** The paper says: "Hence m_i + 3/2 ≥ (3/5)^i (m + 3/2)."
- This needs m_j ≥ ℓ for every j < i. The next sentence ("For every 0 ≤ i < R(m) … hence m_i ≥ ℓ") supplies that.
- So the argument is a simultaneous induction on i < R(m), and it is valid. i < R(m) ⇔ i ≤ ⌊log_{5/3}((m+3/2)/(ℓ+3/2))⌋ ⇔ (5/3)^i ≤ (m+3/2)/(ℓ+3/2), so (3/5)^i(m+3/2) ≥ ℓ+3/2 and m_i ≥ ℓ.
- Exact-power boundary cases are fine because the inequality is non-strict.

**8. NOTE (questions 1(i) and 4).**
- **Non-integer 3H/5.** P_U uses a real exponent, which is harmless. The threshold x_U ≥ 3H/5 is the same as x_U ≥ ⌈3H/5⌉. The step that crosses it sets P_U' = 0 ≤ (9/10)P_U. The terminal statement e_C(U) ≥ (3/5)C(ℓ,2) is a real inequality, and that is exactly the form §3 needs. Tested exactly with ℓ = 4 (3H/5 = 18/5), where K = (4/3)^{18/5} is irrational.
- **Strategy well-defined when all dangers are 0.** Yes. A maximum over a finite non-empty free set exists, ties are arbitrary, and Lemma 1 does not depend on tie-breaking.
- **Where n is used.** The proof uses n in exactly three places:
  - ΣQ ≤ 3^{1−a/2} ≤ 1/n;
  - ΣP ≤ (6/5)(nθ^{(ℓ−1)/2})^ℓ → 0;
  - R(n) ≥ a.

  The paper flags all three. The trivial requirement ℓ, a ≤ n is implicit. Nothing else depends on n.

## Re-derived in full (all hold)

- **(i) Update table.**
  - Chingiz edge in A: Q_A → 0.
  - Bella edge in A: f_A − 1, so ×3 and +2Q_A.
  - Chingiz edge in U: x+1 and f−1, factor (3/4)(6/5) = 9/10, or 0 if the threshold is crossed. Either way the drop is ≥ P_U/10.
  - Bella edge in U: ×6/5, so +P_U/5. A zeroed P_U stays 0 because x_U is unchanged.
- **(ii) Lemma 1.**
  - The danger of every other free edge is non-increasing under a Chingiz edge, in BOTH summands. A set containing the Chingiz edge has its weight zeroed or scaled by ≤ 9/10; any other set is unchanged.
  - So d(e1) ≥ d_0(z) ≥ d\*(z) and d(e2) ≥ d_1(z) ≥ d\*(z). z is free throughout because Bella claims it afterwards, so z ≠ e1, e2.
  - Bella's increase is 2ΣQ + (1/5)ΣP = 2d\*(z) EXACTLY.
  - The design has zero slack.
- **(iii) Initial bounds.**
  - Q-sum: h − a·log₃n = (a/2)(a − 1 − 2log₃n) ≥ a/2, because a − 1 − 2log₃n ≥ ⌈2log₃n⌉ + 1 − 2log₃n ≥ 1. Hence ΣQ ≤ 3^{1−a/2} ≤ 1/n. Also checked numerically for all 2 ≤ n ≤ 200000.
  - P-sum: θ^5 = (64/27)(3125/7776) = 6250/6561 < 1, exactly. ΣP ≤ (6/5)C(n,ℓ)θ^H ≤ (6/5)(nθ^{(ℓ−1)/2})^ℓ, and log(nθ^{(ℓ−1)/2}) ≤ (1 − Cη/2)log n + η/2 → −∞.
- **(iv) Terminal statements.** At the end f = 0. An all-Bella a-set has Q_A = 1. An ℓ-set with x_U < 3H/5 has P_U = (4/3)^{positive} > 1.
- **(v) Averaging.** C(s,ℓ)C(ℓ,2) = C(s,2)C(s−2,ℓ−2), since both count (ℓ-set, pair inside it). Needs ℓ ≥ 2.
- **(vi) Lemma 2.**
  - Average degree in G_C[V_i] is 2e_C(V_i)/m_i ≥ (3/5)(m_i − 1) when m_i ≥ ℓ.
  - The neighbourhood inside V_i excludes v_i, so m_{i+1} ≥ (3/5)(m_i − 1).
  - (3/5)(m−1) + 3/2 = (3/5)(m + 3/2) exactly.
  - v_j ∈ V_j ⊆ N(v_i) for j > i, so the chosen vertices form a clique.
- **(vii) Comparison.**
  - ω(G_B) ≤ a − 1 = ⌈2log₃n⌉ + 1.
  - R(n) = log n/log(5/3) − log_{5/3}(ℓ + 3/2) + O(1) = log n/log(5/3) − Θ(log log n).
  - 1/log(5/3) = 1.957615 and 2/log 3 = 1.820478, a gap of 0.137137. The equivalence holds because log 3 > 2·log(5/3) ⇔ 27 > 25.

**Read but not re-derived:** the history sentence about Guy 1983 (I did not check Guy's original text) and the provenance paragraph.

## Numerical instrument

Files:
- `scripts/instrument.py` (exact `Fraction`). P_U is stored as K·p_U with K = (4/3)^{3H/5}, values are elements α + βK of Q(K), and comparisons are exact via K^5 = (4/3)^{3H}.
- Outputs: `out_main.txt`, `out_qonly.txt`, `out_big.txt`, `out_mutations.txt`.

Method:
- Weights are recomputed from the definition after every move, and the update table is asserted against them, so the table is tested rather than assumed.
- Chingiz plays greedy max-danger with random tie-breaks.
- Bella plays one of five strategies: random, max-danger, min-danger, pure clique-builder (max Q-part), or density attacker (max P-part).

Coverage:
- n ∈ {6, 7, 8, 9} × a ∈ {3, 4} × ℓ ∈ {4, 5}, with both families: 1920 games.
- Q-only regime, where Φ_init < 1 genuinely holds (n = 7..10, a = 4): 480 games.
- n = 10 with (a, ℓ) ∈ {(4, 5), (3, 4)}: 44 games.

Total: 2,444 complete games. Assertions checked:

| Check | Count | Violations |
|---|---|---|
| Chingiz edge: "drop ≥ d(e)" plus Chingiz column of the table | 43,320 edges | 0 |
| Danger of each remaining free edge non-increasing after a Chingiz edge, each summand separately | 607,380 | 0 |
| Bella's increase == 2·d\*(z) EXACTLY, plus Bella column of the table | 19,816 moves | 0 |
| Φ non-increase over complete rounds | 19,816 | 0 |
| Φ non-increase over truncated final Chingiz turns | 1,844 | 0 |
| Φ_end ≤ Φ_init | all games | 0 |
| Initial-sum bounds 3C(n,a)3^−h and (6/5)C(n,ℓ)θ^H | all games | 0 |
| Terminal, contrapositive: an all-Bella a-set ⇒ Φ_end ≥ 1 | 182 games with such a set | 0 |
| Terminal, contrapositive: an ℓ-set with e_C < 3H/5 ⇒ Φ_end > 1 | 2,229 games with such a set | 0 |
| Q-only games with Φ_init < 1: Bella never completed K_a | 480/480 | 0 |

Negative controls (`mut:*` modes). Each mutation must be caught, and each was:
- Chingiz takes 1 edge per turn → 359 round increases.
- Chingiz takes min-danger edges → 202 round increases, plus 14 Bella K_4's despite Φ_init < 1.
- Danger uses P/5 instead of P/10 → 315 "drop < danger" and 240 "Bella ≠ 2d\*".
- P base 4/3 replaced by 5/4 → 6130 table violations.
- Q base 3 replaced by 2 → 739 table violations, plus 187 "Bella ≠ 2d\*" and 48 initial-bound violations.

In `out_mutations.txt` the digits are stripped from the violation-kind labels, so for example "Phi_init< yet" means "Phi_init<1 yet".

`scripts/analytic.py` (output in `out_analytic.txt`) checks:
- θ^5 = 6250/6561 exactly; θ = 0.9903347, η = 0.0097123.
- Leading constants and the n0 estimate from item 1.
- The averaging identity for 2 ≤ ℓ ≤ s < 60: no failures.
- The Lemma 2 worst-case recursion m_{i+1} = ⌈(3/5)(m_i − 1)⌉, using the exact integer R(m), for 2 ≤ ℓ < 80 and ℓ ≤ m < 4000: 2,465,555 steps, 0 failures. A float floor(log) evaluation of R misfires on 9 of the 117 cases where the ratio is an exact power of 5/3; that is an instrument artifact, so the exact R is used.
- The greedy clique on 35 actual graphs with every ℓ-set ≥ 3/5 dense (n = 14..17, ℓ = 3..5, R = 3), choosing adversarially the at-least-average vertex of smallest degree: 0 failures in degree bound, clique property, size ≥ R, or averaging for s ∈ [ℓ, ℓ+3] ∪ {n}.

**Limitation.** At small n the P-family alone makes Φ_init ≫ 1, so the direct implication "Φ < 1 ⇒ (1)" is non-vacuous only in the Q-only runs. For the P family it is tested only in contrapositive form, which is non-vacuous (2,229 games).

**Literature fetched:**
- `dl/masp24.pdf` and `dl/masp24.txt`: arXiv 2410.18304v2.
- `dl/p778.html`: erdosproblems.com/778, fetched via Hetzner because Cloudflare blocks exe.dev.
- Cambie–Provoost was read from `/tmp/erdos778/lit/cp25.txt`.
