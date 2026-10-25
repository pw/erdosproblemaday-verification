# Main seat's own reading of "Cycle–clique Ramsey numbers" (OpenAI, 25 Sep 2026) — §2 through §9, line by line
21:00Z erdos seat, 2026-10-20, Claude Opus 5.5 (Team seat 3). Read from the LaTeX source in the release (same text as the PDF,
sha256 366fc1d9…); printed section numbers. Verdict: **HOLDS AS READ** — every step below was re-derived; no gap, no fatal error.
Where a step is only a computation I re-did it (numbers given). Seats P (§5–8), F (§9 + code) and W (sources) read independently.

## §2 Minimal counterexample (Lemmas 2.1, 2.2)
- k = m−1 ≥ 3 and 2 ≤ a = n−1 ≤ k is exactly the range m ≥ n ≥ 3, (m,n) ≠ (3,3): (3,3) is k = 2, and m = 3 forces n = 3.
- Lemma 2.1: b = 0 empty; b = 1 complete, ≤ k vertices since K_{k+1} ⊇ C_{k+1}; 2 ≤ b < a by minimality of a. Correct.
- Lemma 2.2: α(G − N[I]) ≤ a − |I| (independent sets of the remainder extend I), Lemma 2.1 applies for every 0 ≤ a−|I| ≤ a−1
  (including |I| = a), so |N[I]| ≥ ka+1 − k(a−|I|) = k|I|+1. Correct.

## §3 Large clique, max{3,⌊k/2⌋} ≤ t ≤ k (Theorem 3.1)
- Triangle: R(K3,K_{a+1}) ≤ (a+1)(a+2)/2 ≤ ka+1 ⟺ a+3 ≤ 2k, true as a ≤ k, k ≥ 3. Recurrence r_b ≤ b + r_{b−1} proved correctly.
- Proposition 3.3 (layer interface), k ≥ 8, s = ⌊k/2⌋, no K_s:
  parity unions of maximum independent sets of same-parity BFS layers are independent (edges join layers differing by ≤ 1); p_0 = 1,
  p_i ≤ k; closed nbhd of the p_{i−1}-union lies in D_0..D_i ⇒ Σ_{j=1}^{i}|D_j| ≥ k·p_{i−1}; Σ α(D_j) = p_i + p_{i−1} − 1.
  Even k = 2s: if every nonempty layer had |D_j| < sα(D_j) then p_i ≥ p_{i−1} + 2, p_s ≥ 2s+1 > k. Odd k = 2s+1: if all
  |D_j| ≤ sα(D_j) then p_i ≥ p_{i−1} + 1 + ⌈p_{i−1}/s⌉, so p_{s−1} ≥ 2s−1 > s, last increment ≥ 3, p_s ≥ 2s+2 > k. Correct both parities.
  Minimal H in the good layer: not complete (no K_s) ⇒ α ≥ 2 ⇒ |H| ≥ k; connected (components would sum to a failure); nonbipartite
  (α ≥ |H|/2 contradicts |H| ≥ sα with s ≥ 4); expansion |N_H[I]| ≥ s|I| (strict unless R empty and k even) from minimality applied to
  R = H − N_H[I]; δ(H) ≥ s. All correct.
- Lemma 3.4 (longest path ≥ min{|F|, 2d+1}): index sets of size ≥ d each inside {1..r−1} with r−1 ≤ 2d−1 must meet; the three cases
  (j = 1, j = r−1, 2 ≤ j ≤ r−2) each give a cycle on the path's vertices; connectivity extends it. Correct.
- Lemma 3.5 (coloured path of every length 1 ≤ ℓ ≤ 2s−2): I re-derived every step — y, z of different colours with common neighbour
  x (even walks in a connected nonbipartite graph); K = component of x in H−{y,z}, δ(K) ≥ s−2; no path of order ≥ ℓ from x in K
  (else prefix y or z); r ≥ s−1 kills ℓ ≤ s−1; endpoint set E is a clique (two nonadjacent ends would have |N[{a,b}]| ≤ r+2 ≤ 2s−1);
  Pósa rotation ⇒ successor of every K-neighbour of an end is an end ⇒ d_K(e) ≤ |E| ⇒ s−2 ≤ |E| ≤ s−1; E is a final segment;
  N_K(w) ⊆ (E−w) ∪ {u} for w ≠ w0; u has ≥ 2 neighbours in E (case |E| = s−2 by degree count (s−3)+3 = s; case |E| = s−1 else
  E ∪ {y} or E ∪ {z} is a K_s); some w ∈ E sees both y, z; K is not a clique and |K| ≥ 2s−2; K−E connected; the longest path R from
  u in K−E has |R| ≥ s−1, and |E| + |R| ≥ 2s−2 ≥ ℓ (the case |E| = s−2, |R| = s−1 is killed by the pair {v, w}, |N| ≤ 2s−1).
  Correct.
- §3.2: p = 1 ⇒ a path of order k in H closed through the common parent; p ≥ 2 ⇒ ℓ = k+1−2p ∈ [1, 2s−2] (from 2 ≤ p ≤ s,
  k ∈ {2s, 2s+1}) and the coloured path plus the tree path is a C_{k+1}. Correct.

## §4 k = 3, 4 (Proposition 4.1)
- k = 3: U_i nonempty, pairwise disjoint and anticomplete (C4s q_i u q_j q_h and q_i u v q_j), one vertex from each U_i is
  independent ⇒ a = 3, |F| = 7; U_i cliques of size 1–2; W ≠ ∅; w ∈ W has ≤ 1 neighbour per U_i (C4 w u q_i v) and misses
  vertices in at most one U_i ({w,u,v,q_h} would be independent of order 4) ⇒ ≥ 2 singleton U's; both size patterns (1,1,2) and
  (1,1,1) close a C4 through two w's. Correct.
- k = 4, K4 present: N_F[U_i] pairwise disjoint (three C5 patterns with 1, 2, 3 interior vertices), each ≥ 4 ⇒ 16 > 4a−3 ≤ 13. Correct.
- k = 4, ω = 3: disjoint-exterior case ⇒ U_i cliques of size 2 ⇒ the triangles T_i = {q_i,u_i,v_i} force |N_F[U_i]| ≥ 6, 18 > 14;
  overlapping triangle ⇒ exactly one overlapping pair, I independent; the class table (I,A,B,D) with the stated triangle neighbours
  gives disjoint closed neighbourhoods (checked: each of the six rows closes one of §4's two C5 patterns); counts r = 1 → 15, r ≥ 3 → 15, r = 2 → 11
  and A = B = ∅, D a 2-clique; then T = {q1,q2,w} is itself overlapping with exterior sets {q3,z} ⇒ d_F(w) = d_F(z) = 2 ⇒
  |N_F[I]| ≤ 6 < 7. Correct.

## §5 Size test (Lemmas 5.1–5.3)
- 5.1 (2-connected, α ≤ 2 ⇒ Hamiltonian): a⁺ has no neighbour in D when a does; a⁺ ≠ b (b has a D-neighbour); the a⁺b⁺ reroute
  uses exactly the two arcs of C − {aa⁺, bb⁺}. Correct.
- 5.2 (shortening, r ≥ 7): no i(i+2) chord ⇒ all step-4 chords; the cycle 1..r−6, r−2, r−1, r−5, r−4, r−3 omits only 0; joins have
  cyclic differences 4, −4, 4−r ≡ 4; r = 7 instance 1,5,6,2,3,4. Correct.
- 5.3: disconnected ⇒ two cliques ≤ 2t; cutvertex ⇒ |A| = |B| = t and a K_{t+1}; else Hamiltonian, shorten from n ≥ k+1 down to
  k+1 (each intermediate r ≥ k+2 ≥ 7). Correct.

## §6 Optimal path systems (Lemmas 6.1–6.4, Corollary 6.5)
- 6.1: u = k+1−q−v ∈ [0, t−v]; expanded chains + u singletons have q+v+u = k+1 vertices, joined by clique edges into one cycle;
  the 1-path and 2-path-with-singleton cases handled. Correct.
- (6.3) e ≤ L ≤ k−t, |S| = t+L ≤ k. 6.2 criterion, 6.3 (≥ k+1−|S| exterior neighbours): correct.
- 6.4: meeting balls ⇒ walk of ≤ r+s+2 edges, adjacent balls ⇒ ≤ r+s+3; loop-erasure keeps ≥ 1 interior vertex because x, y ∈ X
  occur only at the ends and every interior walk vertex is outside X. Part 2 correct. 6.5 correct.

## §7 Short paths between representatives (t ≥ 9)
- Representatives ρ(q) are distinct; Lemma 7.1 (replacement) keeps a linear forest: after deleting the incoming edges each target has
  degree ≤ 1 and the two targets lie in different components (same chain: deleting the later target's incoming edge separates them);
  amount L+d, e+1−r paths; the old edge qq′, if any, was one of the deleted ones. Correct.
- 7.2 one-vertex detours: amount L+1 contradicts maximality or lands in Lemma 6.1's interval (v ≤ t). Correct.
- (7.1) |B_1(x;S)| ≥ k−|S|+t, +1 if some y ∈ S∖R is missed by all of B_0. Correct.
- 7.3: B_2 not a clique (else B_1 = B_2 = K_t with |S| = k, every vertex attains both degree bounds, so sees x ⇒ K_{t+1});
  independent pair in B_1 ⇒ |B_2| ≥ 2k−|S|+t ≥ k+t > max(k,2t) when t < k ⇒ triple. Correct.
- 7.4: 2t > k closes immediately; else k ∈ {2t, 2t+1}; |S| < k gives |B_1| > t; |S| = k with e ≥ 2: the next vertex y after an
  interior representative is not in R and is missed by its outside neighbours (consecutive-vertex detour); e = 1: reverse the one
  nonsingleton chain, its new start y ∉ R is missed by the outside neighbours of every singleton representative. ⇒ two
  noncliques ⇒ 2t+2 > k. Correct. (t ≥ 9 is not actually needed inside 7.4's proof.)

## §8 Excluding t ≥ 9 (Lemmas 8.1–8.3, Proposition 8.4)
- 8.1: the inclusion-minimal subcollection has amount h+j, 0 ≤ j ≤ 5, and w > t−j forces j ≥ 1, 2r ≥ w ≥ t−j+1. If every selected
  amount were ≥ j+2: (t−j−1)(j+2) ≤ 2(k−t) ≤ 2t+2; the left side is concave in j with end values 3(t−2), 7(t−6), which exceed 2t+2
  by t−8 and 5t−44 > 0 for t ≥ 9. So some amount is exactly j+1; deleting it gives amount h−1 ⇒ L = h−1, tie-break ⇒ r = e+1, all old
  paths kept, j = d−1, new amount d, old amounts ≥ d. Correct.
- 8.2 classification: v + a ≥ t−d+2; d·⌈(t−d)/2⌉ ≤ d·e ≤ L ≤ t+1. d = 2 → v ≥ t−2; d = 3 → t ≤ 11, t = 10 dies (12 > 11), t = 9: e = 3,
  t = 11: e = 4, v = 2e = t−3, a = 2; d = 4 dies (t ≤ 9, 12 > 10); d = 5 → t = 9, e = 2, v = 4, L = 10, k = 19, a = 2; d = 6 dies (t ≤ 9,
  12 > 10). The three alternatives are distinguished by v (≥ t−2, = t−3, = t−5), so whichever holds governs every short path in every
  orientation. Correct.
- 8.3: ≥ 2 nonsingleton chains (Alt. 1 with one chain: v ≤ ⌊(t+1)/2⌋+1 < t−2 for t > 7); reversing a second chain adds a clique
  vertex missed by B_0(x) ⇒ |B_1| ≥ t+1, |B_2| ≥ k+1 ⇒ triple when k ≥ 2t. Correct.
- 8.4 packings: Alt. 1, c ≥ 1: k ≥ 2t−2, two further chosen representatives miss B_1(x) ⇒ |B_2| ≥ k+3 ≥ 2t+1 ⇒ triples,
  3(t−c) ≥ 3t−6 > 2t+1 ≥ k (t ≥ 8). Alt. 1, c = 0: e = ⌈t/2⌉, k ≥ 2t; t even: matching, ≤ one amount-3 path, t or t−1 bases;
  t odd: L = t+1, one two-edge chain, t−1 bases; same-path pairs a, b are excluded by rerouting the step ab (a path removed ⇒ 8.1);
  3(t−1) > 2t+1. Alt. 2: k ≥ (5t−9)/2 ≥ 2t, t−2 bases, 3(t−2) > 2t+1. Alt. 3: radius-2 balls at 4 incident bases, radius-1 at 5 missing
  bases; forbidden ranges 1..6 / 1..5 / 1..4 are exactly what Lemma 6.4 needs for (2,2), (2,1), (1,1); 4·3 + 5·2 = 22 > 19. Correct.

## §9 Finite stage (Proposition 9.1 and Lemmas 9.2–9.10)
- Domain: for t ≤ 8 the clique bound gives k ≤ 17; with k ≥ 5 and max{3,⌊k/2⌋} ≤ t ≤ min{8,k} this is 42 pairs (recounted).
- Lemma 9.2 (coverage): reversal-normalised, sorted chain tuples are a complete invariant of weighted linear forests. Recounted by our
  own brute-force enumerator (`count_patterns.py`): every row of Table 1, 42 pairs, 3,099 patterns; negative control (budget + 1) gives
  5,735. The Lean's hard-coded lists (`Patterns{k}x{t}.lean`) equal our enumeration as sets, all 42 pairs, no duplicates, canonical form
  (`lean_pattern_lists.py`; a budget−1 mutant fails 38/42 pairs — the 4 with t = k have zero budget either way).
- Lemma 9.3 labels: correct (consecutive labelling; increasing routes).
- Lemma 9.4 extension rule: the two extension segments are disjoint in every case (same old path forces z = a, w = b and the segments
  {a..x}, {y..b}; different paths can meet only at a common clique endpoint, i.e. z = w, excluded); discarding the paths with x or y in
  their interiors leaves pairwise disjoint interiors; adding zw keeps a linear forest; amount q+d; the interval (9.7) then contradicts
  maximality / tie-break below h and Lemma 6.1 at or above h. Restricting to d ≥ 1 is conservative (d = 0 can give an empty-interior
  "path"). The worked example k = 5, t = 3, P = ((),(2)) re-done by hand: d ∈ {1, 2} forbidden, both close 6-cycles. Correct.
- Lemma 9.5 (required path of length ℓ ⇒ k−ℓ forbidden): ℓ+1 + (k−ℓ) = k+1 vertices. Correct. 9.6 inheritance: correct.
- Lemma 9.7 ball bounds: b_0 from certified non-neighbours; b_0 ≥ t ⇒ pair; A_r vertices see nothing in B_{r−1} (Lemma 6.4(2));
  expansion on a u_{r−1}-set in B_{r−1}; the exceptional clause (9.11): a t-clique ball whose vertices hit both degree bounds is
  complete to X ∖ A_r ∋ i ⇒ K_{t+1}. Correct.
- Lemma 9.8 packing + the radius-pruning argument + the branch-and-bound search: correct.
- Lemma 9.9 (trial edge / trial vertex): the trial graph is realised by the actual edge or the actual interior vertex z ∉ S; old
  constraints transfer by 9.6; contradiction ⇒ prohibition relative to S (for every choice of z). Prop 9.10: batch soundness
  (all trials of a round use the old matrix) and termination. Correct.
- §9.6: both released checkers re-run unmodified here (`verify.py`, CPython 3, 197 s, 72 MB): both "complete output agrees",
  "Verified 3099 patterns in all 42 parameter pairs; zero unresolved." Table 2 sums to 3,049 + 50 = 3,099.
- Proof of Theorem 1.1: the upper bound chains §2 → §3 → §4 (k = 3, 4) → §8 (t ≥ 9) → §9 (t ≤ 8), and every (k,t) is covered: k ≥ 18
  forces t ≥ 9. Lower bound (n−1 disjoint red K_{m−1}) and R(C3,K3) = 6 standard. Correct.

## Small observations (exposition only)
- Lemma 7.4 assumes t ≥ 9 but its proof uses only t ≥ 4 (e = 1 case needs two singleton chains).
- The release's `lean/formalization.yaml` (its own catalogue of formalized papers) does not list this paper, although `lean/docs/189.md`,
  the comparator challenge and 443 Lean modules are in the same commit.
