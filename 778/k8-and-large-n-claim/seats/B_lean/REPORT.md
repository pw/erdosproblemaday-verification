STATEMENT MATCH (asymptotic form only: Bob/Chingiz wins for every n >= 3^158; this is not the full "n > 3" question)

Seat B_lean. Source audited: /tmp/erdos778/lean/src/erdos12-lean-v0.1.0/ (SHA256SUMS: all 23 files OK). No build run; the axioms claim is left to the kernel replay.
Scratch checks in this folder: arith.py (exact arithmetic), protocol_check.py (the Game.lean protocol checked against a direct game tree).

## Verdict on `Erdos12.erdos_one_two_main` (Main.lean:44-48)

    theorem erdos_one_two_main :
        ∃ N : ℕ, ∀ n : ℕ, N ≤ n → ∃ σ : Strategy n, WinningStrategy σ

Read with Game.lean, this says: for every n >= N, Chingiz (Bob) has a strategy in the literal (1:2) edge-claiming game on K_n that ends with strictly larger final clique number than Bella's (Alice's), whatever Bella plays. The witness is N = explicitThreshold = 3^158 (Main.lean:46). The sharper form is Main.lean:25-26, `greedyStrategy_wins_above_threshold : explicitThreshold ≤ n → WinningStrategy (greedyStrategy n)`.

## Task 1: Game.lean checklist

(a) NOTE, correct. Game.lean:24-25 `allEdges n := (Finset.univ : Finset (Fin n)).powersetCard 2` is every 2-subset of Fin n, so the board is the edge set of K_n.

(b) NOTE, correct. Bella moves first: Game.lean:49-50 `first (e) (he : e ∈ allEdges n) : RoundReachable σ {e} ∅`.
- A round is Chingiz, Chingiz, Bella (Game.lean:51-63). Chingiz's first edge is `σ bella chingiz`, which must be free (:53). His second edge is `σ bella (insert (σ bella chingiz) chingiz)`, so it is chosen from the position after his first edge and must be free there (:54-55). Bella's edge `e` must be free after both of his edges (:56-59).
- `Terminal` (:69-90) covers all three ways the last Chingiz pair can end: zero edges (`afterBella`, :71-74), one edge (`afterFirst`, :75-79) and two edges (`afterSecond`, :80-90). Each requires `freeEdges … = ∅`, so every edge is coloured at the end and no player can pass.
- This matches the paper's "two, or all remaining edges if fewer than two remain".

(c) NOTE, correct. Bella's move is a constructor argument, `(e : Edge n) (he : e ∈ freeEdges …)` (:56-57), and her opening is any `e ∈ allEdges n` (:49).
- `WinningStrategy` quantifies over every derivation of `Terminal σ bella chingiz` (:131-133), so it covers every sequence of legal Bella moves. That includes every adaptive Bella strategy.
- `ChingizWins` depends only on the final position, so quantifying over final positions rather than over plays loses nothing.

(d) NOTE, no loss of generality. `Strategy n := Finset (Edge n) → Finset (Edge n) → Edge n` (:36) is positional.
- Positional strategies are a subclass of history-dependent ones, so a positional winning strategy is a winning strategy.
- The position also reveals which half of his pair Chingiz is playing: |chingiz| = 2|bella|-2 for his first edge and 2|bella|-1 for his second.
- The greedy strategy is positional: Potential.lean:96-100 reads only `bella` and `chingiz`, through `freeEdges bella chingiz` and `danger bella chingiz`.

(e) NOTE, no vacuous win is possible for a legal strategy. Hand proof:
- Every RoundReachable position is legal, by induction. Every constructor carries its freeness hypotheses. TerminalProperties.lean:44-51 proves this for the greedy strategy, and the same proof works for any σ.
- Start from a reachable position (b,c). If free(b,c) = ∅, the play ends in `afterBella`.
- Otherwise, LegalStrategy (Game.lean:39-41) puts c1 in the free set. If nothing is free after c1, the play ends in `afterFirst`.
- Otherwise (b, c∪{c1}) is legal (`legal_insert_chingiz`, TerminalProperties.lean:16-28), so c2 is free. If nothing is free after c2, the play ends in `afterSecond`.
- Otherwise every free e gives a `round`. A round removes three free edges, so every play reaches a `Terminal` after finitely many rounds.
- Conversely, every `Terminal` position is the final position of a real play.
- A strategy that returns a non-free edge does escape: its plays never reach `Terminal`, so it would win vacuously. The `LegalStrategy` conjunct of `WinningStrategy` (:132) rules this out, so that conjunct matters and it is present.
- Model check (protocol_check.py): I transcribed the rules literally for n = 2..5 with two legal positional strategies. The set of `Terminal` positions equalled the set of leaves of a direct move-by-move game tree in all 8 cases (1/1/3/3/12/12/55/132). With an illegal σ at n = 4, `Terminal` was empty and 6 plays got stuck.
- The Lean source contains no adequacy or non-emptiness lemma for `Terminal`. Adequacy rests on reading :47-90, which I did.

(f) NOTE, correct, with no off-by-one.
- `IsClique` (:93-94) requires every 2-subset of `s` to be claimed. `HasClique claimed k` (:97-98) asks for a clique of exactly k vertices.
- `cliqueNumber := Nat.findGreatest (HasClique claimed) n` (:101-103) is the largest k <= n with a k-clique. A clique has at most n vertices because s ⊆ Fin n, so the cap at n loses nothing, and k = 0 always holds.
- The bridge lemmas at :105-124 show it is exactly the maximum clique size.
- Empty sets and singletons count as cliques, so ω >= 1 for both players once n >= 1. That is the standard convention for ω, applies to both sides, and does not change the comparison.

(g) NOTE, correct. :127-128 `cliqueNumber bella < cliqueNumber chingiz` is strict, as the problem requires.

(h) NOTE, correct.
- Main.lean:10 `explicitThreshold : ℕ := 3 ^ 158`, and Main.lean:46 `refine ⟨explicitThreshold, ?_⟩`.
- Potential.lean:21 `scale n := Nat.log 3 n`, i.e. ⌊log_3 n⌋. Main.lean:12-23 gives scale n >= 158 and 3^scale n <= n.
- 3^158 is about 2.4·10^75.

## Task 2: trust surface

NOTE, clean.
- Searching every .lean file finds 0 hits for `sorry`, `admit`, `axiom`, `native_decide`, `decide` (in any form), `unsafe`, `implemented_by`, `extern`, `opaque`, `partial`, `set_option`, `instance`, `attribute`/`@[...]`, `macro`/`syntax`/`elab`/`notation`, `#eval` and `run_cmd`.
- `noncomputable` appears only at Game.lean:101 (`cliqueNumber`) and Potential.lean:96 (`greedyStrategy`).
- The `classical` tactic is used at Game.lean:102,108,116, LocalPotential.lean:21,27, Density.lean:36 and CliqueExtraction.lean:27,79. `Classical.choose` is used at Potential.lean:98,106,114 for tie-breaking among maximum-danger edges.
- Numerical facts are proved with `norm_num`, `omega`, `linarith`, `positivity` and `ring`. ExtractionThreshold.lean:170-172 runs `norm_num` on numbers around 10^230. That uses kernel arbitrary-precision Nat arithmetic, which is standard and is not `native_decide`.

NOTE, pins verified.
- lakefile.toml requires only mathlib `rev = "v4.24.0"`, with no `moreLeanArgs`, precompile or option overrides.
- lake-manifest.json pins mathlib `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`. `git ls-remote` confirms that is tag v4.24.0.
- All 8 inherited packages (plausible, LeanSearchClient, importGraph, proofwidgets v0.0.74, aesop, Qq, batteries, Cli) match mathlib's own lake-manifest.json at that commit, which I fetched.
- lean-toolchain is `leanprover/lean4:v4.24.0`, the same as mathlib's.

NOTE, not verified here. The README and RELEASE_CHECKS claim `#print axioms` reports only propext, Classical.choice and Quot.sound. That is left to the replay.

## Task 3: Lean against the paper

The strategy, weights and argument are the paper's. The changes are integer parameter choices and an explicit final inequality in place of the asymptotics. It is a faithful finitization, not a different argument.

| Paper | Lean | Relation |
|---|---|---|
| a = ⌈2 log_3 n⌉ + 2 | `smallSize n = 2·scale n + 4` (Potential.lean:24) | smallSize is between a and a+2, so it is never smaller. At k = 158, a is 318–320 and smallSize is 320. |
| ℓ = ⌈C log n⌉ with Cη > 2 | `largeSize n = 250·(scale n + 1) + 1` (:27) | This means C ≈ 250/ln 3 ≈ 227.6 and Cη ≈ 2.21 > 2, with η = (1/5)ln(6561/6250) ≈ 0.009712. ℓ ≡ 1 (mod 5), so 5 divides H. |
| 3H/5 | `largeTarget n = 3 * (pairCount (largeSize n) / 5)` (:33) | Exactly 3H/5, by InitialPotential.lean:207-210 and arith.py. The paper's fractional exponent becomes an integer. |
| Q_A = 3^{-f_A}, or 0 if A has a Chingiz edge | `qWeight` (:53-56) | Identical. |
| P_U = (4/3)^{3H/5-x}(5/6)^{f} while x < 3H/5, else 0 | `pWeight` (:59-64) | Identical. |
| d(e) = Σ_{A∋e} Q_A + (1/10) Σ_{U∋e} P_U | `danger` (:89-90) with `qDanger` and `pDanger` (:79-86) | Identical. |
| Take a maximum-danger free edge, each time | `greedyStrategy` (:96-100) via `Finset.exists_max_image` | Identical. Ties are broken by a fixed classical choice, which the paper allows. The danger is recomputed before the second edge. |
| Lemma 1 | `greedy_round_nonincrease` (StrategyProof.lean:24-57), using `pCore_chingiz` (CoreWeights.lean:50-67, which includes the cutoff case) | Same proof. Bella's increase is shown to be at most 2·danger rather than exactly equal, which is enough. |
| Paper: if the game ends on Chingiz's move, Φ only decreases | `terminal_potential_lt_one` (StrategyProof.lean:69-93) | Same. |
| Initial Φ = o(1) | `q_numeric` <= 1/9 (InitialPotential.lean:169-205) and `p_numeric` < 8/9 (:231-280) | Explicit. Uses C(n,r) <= n^r and n < 3^{k+1}. `p_numeric` is the paper's (n θ^{(ℓ-1)/2})^ℓ bound in the form (3·(6250/6561)^25)^{(k+1)ℓ}, where 3·(6250/6561)^25 ≈ 0.891. Both hold once n >= 3. |
| (1): every a-set contains a Chingiz edge, and every ℓ-set has at least (3/5)·C(ℓ,2) Chingiz edges | `terminal_small_sets_hit` and `terminal_large_sets_dense` (TerminalProperties.lean:99-136) | Same. |
| Density lifted from ℓ-sets to every s-set with s >= ℓ, by averaging over ℓ-subsets | `dense_of_dense_erasures` and `dense_above` (Density.lean:70-130), one vertex deletion at a time | Equivalent double count. |
| Lemma 2 recursion, m_{i+1} >= (3/5)(m_i - 1), shifted by 3/2 | `exists_large_neighbors` and `clique_from_dense_recurrence` (CliqueExtraction.lean:120-257), shifted to 2m+3 | Same recursion. |
| Final step: R(n) ~ log n/log(5/3) - O(log log n) against a-1 ~ 2 log n/log 3 | Chingiz's target is smallSize itself (ExtractionThreshold.lean:237-263). This needs 5^{2k+3}(2ℓ+3) <= 3^{2k+3}(2n+3), which follows from `extractionGood k : 125·25^k(500k+505) <= 2·27^{k+1}` (:167-168) for k >= 158 | The 27 > 25 comparison lives here. k = 158 is the least k for which `extractionGood` holds (arith.py), so the threshold is tight for this inequality. "Unoptimized" refers to the constants 250 and +4. |

Things the paper states that the Lean does not prove:
- NOTE: the asymptotic bounds in the abstract, ω(G_C) >= log n/log(5/3) - O(log log n) and ω(G_B) <= 2 log n/log 3 + O(1), are not formalized. The Lean proves only ω_B <= 2k+3 (TerminalProperties.lean:138-153) and ω_C >= 2k+4 (ExtractionThreshold.lean:254-263), with k = ⌊log_3 n⌋ >= 158. Theorem 1 does not need the asymptotics.
- MINOR: some imported files are not used by the main theorem, though the docs present them as part of the formalization.
  - Threshold.lean's `twenty_five_lt_twenty_seven` and `ratio_square_lt_three` (:65-70) are unused.
  - GreedyPotential.lean as a whole (the abstract `potential_nonincrease_in_round`, :133-157) is unused.
  - Weights.lean is unused apart from `theta_fifth`.
  - Erdos12.lean imports them, and README/FORMALIZATION_MAP describe them as "companion lemmas". They carry no weight. The real 25/27 comparison is `extractionGood`.

## Other findings

- MINOR: README.md:19 says "the last Chingiz pair is truncated if fewer than three free edges remain". That is imprecise. After Bella's move, the pair is truncated only if fewer than two free edges remain; with exactly two left, Chingiz takes both and the game ends. Game.lean is correct, so this affects the documentation only.
- MINOR: `WinningStrategy` is vacuously true for every legal σ when n <= 1. `allEdges` is empty, so `first` cannot fire and there is no `Terminal`. But in the real n = 1 game ω_B = ω_C = 1 and Chingiz does not win. This does not touch the main theorem (N = 3^158), and every n > 3 has n >= 2. Anyone reusing these definitions for small-n statements should still be aware of it.
- NOTE: `greedyStrategy` is noncomputable (classical tie-breaking, and sums over C(n, 39751) sets). The theorem proves existence only and provides no executable strategy. That is enough for the claim.
- NOTE: `LegalStrategy` quantifies over every legal position, not just reachable ones. This is a stronger requirement than needed, harmless, and the greedy strategy meets it (Potential.lean:117-119).

## Task 4: what this does NOT settle for Erdős #778

- Q2 asks whether Bob wins for every n > 3. The Lean proves it only for n >= 3^158 ≈ 2.4·10^75. Every n in [4, 3^158) remains open as far as this artifact goes: no finite cases are checked, and the argument cannot reach below k = 158.
- It says nothing about the unbiased (1:1) game in the first question of #778.
- It says nothing about the degree variant.
- It does not give the paper's asymptotic clique-number estimates. It gives only the explicit comparison at scale k.

FATAL: none. GAP: none.
