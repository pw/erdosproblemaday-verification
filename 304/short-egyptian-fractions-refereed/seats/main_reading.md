# Main seat (18:00Z erdos cron seat, 2026-10-21, Claude Opus 5.5) — own reading of printed §2, §5, §6

Read from the LaTeX source (elementary.tex, descent.tex, counting.tex), numbers cited as printed.

## §2 From a dense set to every numerator — HOLDS AS READ
- Lemma 2.2 (Takenouchi): 2/(2p) = 1/(p+1) + 1/(p(p+1)) (denominator-sum increase (p−1)², needs p ≥ 2) and 2/(2p+1) = 1/(p+1) + 1/((p+1)(2p+1))
  (increase 2p², p ≥ 1) both check; total < 1 excludes a 1 and a repeated 2; finitely many nondecreasing k-lists with sum x (first ≤ k/x) ⇒ terminates.
- Lemma 2.3 (greedy): z = ⌈C/A⌉, A' = Az − C ∈ [0, A), C' = Cz ≤ C² (z ≤ C as A ≥ 1); x − 1/⌈1/x⌉ < x²/(1+x); x₁ < 1/2, x_{j+1} ≤ x_j²
  ⇒ x_j ≤ 2^{−2^{j−1}}; not stopped ⇒ x_j > 1/T; step bound follows. First crossing: previous C < T ⇒ new C < T².
- Proof of Thm 1.1 from Prop 2.1: T = e^{D_C S} > b (D_C > 1); AM < b·e^{D_M S} < X = e^{(D_M+2)S}; n = gAM ∈ [X/2, X]; at most 2|H| ≤ X/4 of the
  n − 1 splits touch H, n − 1 > X/4 ⇒ a good split; both parts ≤ n − 1 < X lie in {1..⌊X⌋}; sum of the two expansions = n/(MC) = gA/C;
  multiplying denominators by g gives A/C; prefix + tail, Lemma 2.2 on a/b < 1. Uniform in a.
- Lower bound: (b−1)/b with k terms + 1/b, sorted, L_j ≤ s^{2^j−1}, d_j ≤ s^{2^{j−1}}, b ≤ (k+1)^{2^k}, log log b ≤ (1+log 2)k. (The Lean uses c₁ = 1/2 < 1/(1+log 2).)

## §5 Propagating the exceptional sets — HOLDS AS READ
- Bad-pair count (5.7): u ∈ H_j ∩ (Y, X] non-exceptional has ≥ ρ|I_j|/2 indices with h ≤ Y; each such h ∈ H_{j+1} (else u ∈ G_j);
  a pair (h, i) has ≤ d_X(C_j t + h) predecessors since u | C_j t + h = uz. Hölder with Lemma 3.1 gives
  Σ_{h∈H_{j+1}} d_X(N+h) ≤ Y e^{S^{1/4}/r} δ_{j+1}^α; dividing by X, Y = ρX cancels 1/ρ; ρδ ≤ δ^α ⇒ δ_j ≤ ε + Aδ_{j+1}^α (5.9).
- Unrolling from δ_d = 0: term i is A^{(1−α^i)/(1−α)} ε^{α^i} ≤ A^r ε^{α^d}; α^d ≥ S^{−1/4} by r ≥ 8K_d; so
  δ_0 ≤ d·exp(2rS^{1/4} − c_* m S^{−1/4}) → 0 as m ≥ S/(2 log S). Checks.
- Range checks: u ≤ X_0 = e^{D_X S} < MC (M > e^S, C ≥ e^{4D_X S}); u ≤ e^S < M at C_j = 1; C_d = 1.

## §6 Counting representations of one — HOLDS AS READ
- Lemma 6.1 odd replacement 2/m = 2/(m+1) + 2/(m(m+1)) checks; invariant (a multiple of odd Q survives) and lex termination check.
- (6.1) 1/n = 1/(n+d) + 1/(n+n²/d), n < n+d < 2n < n+n²/d; collision count τ(n) − 1 − 2(s−1); n+d recovers d ⇒ distinct sets.
- (6.2) padding injective (inverse: delete the two largest, reinsert second largest − 1). r = ⌊exp(k/(2B))⌋ ⇒ ℓ ≤ k/2, F(k) ≥ 2^{r−1}.
- Upper bound n_i ≤ k^{2^{i−1}}, F(k) ≤ k^{2^k−1}: the same argument as §2's lower bound. Checks.

Nothing to add to seats U and P. (Seat P's O2/O3 on §6 phrasing: agreed, exposition only.)
