# Seat P (PROOF) — referee report on §5–§8 of "Cycle–clique Ramsey numbers" (OpenAI, 25 Sep 2026)

VERDICT: HOLDS AS READ — §5, §6, §7, §8 (Lemmas 5.1–5.3, 6.1–6.4, Cor 6.5, Lemmas 7.1–7.4, 8.1–8.3,
Prop 8.4) are correct as printed; only EXPOSITION remarks (E1–E5 below). No FATAL, no GAP. The hand-off to §9
(t ≤ 8 ⇒ (9.1): 5 ≤ k ≤ 17, max{3,⌊k/2⌋} ≤ t ≤ min{8,k}) is complete, and §9.1's patterns cover every optimal
system by construction (3,099 patterns over 42 pairs, recounted independently).

Summary of evidence: every lemma read line by line with every inequality, vertex count and case split re-done by
hand; arithmetic of §8 brute-forced for t = 9..70; an independent exhaustive model check of Lemmas 7.1/8.1/8.2/8.3
and Prop 8.4's separation+counting claims over ALL weighted path systems for t = 9,10,11,12 and all k ∈ [t,2t+1]
(≈ 79 million replacement systems), with a positive control at t = 8 that fails exactly as Lemma 8.1 predicts;
Lemma 5.3 brute-forced over all α ≤ 2 graphs on ≤ 11 vertices with a negative control.

Scope: printed §5 (Lemmas 5.1–5.3), §6 (Lemmas 6.1–6.4, Cor 6.5), §7 (Lemmas 7.1–7.4 and the unnumbered
degree estimate (7.1)-display after Lemma 7.2), §8 (Lemmas 8.1–8.3, Prop 8.4), and the hand-off to §9.1
(Prop 9.1, Lemma 9.2). Read from the LaTeX source (same text as the PDF); lemma numbers taken from
/tmp/oaimath/189/paper.txt. Scripts + outputs in /tmp/oaimath/189/seats/seatP_work/.

Statement relied on from §3 (main seat already checked it), quoted:
"Theorem 3.1. Let k ≥ 3 and 2 ≤ a ≤ k ... |V(G)| = ka+1, α(G) ≤ a, C_{k+1} ⊄ G ... |N_G[I]| ≥ k|I|+1 for every
nonempty independent set I ... Then its maximum clique size t satisfies max{3, ⌊k/2⌋} ≤ t ≤ k."
From §2: Lemma 2.2 (expansion |N_G[I]| ≥ k|I|+1, δ(G) ≥ k, α(G) ≤ k).
Consequence used throughout §8: t ≤ k ≤ 2t+1, so L ≤ k−t ≤ t+1.

## Running notes (written as I go)

### §5 From size to independence — checked line by line: CORRECT

* Lemma 5.1 (2-connected, α ≤ 2 ⇒ Hamiltonian). Checked every step. "If a ∈ V(C) has a neighbor in D, then
  a⁺ has none" — correct (a path a,x,…,y,a⁺ with x,y ∈ D, possibly x = y, has nonempty interior). "a⁺, b⁺ are
  distinct, neither equals a or b" — a⁺ ≠ b because b has a neighbour in D and a⁺ has none; correct. The
  rerouting a →P→ b →(C backwards)→ a⁺ → b⁺ →(C forwards)→ a uses exactly the two arcs of C − {aa⁺, bb⁺};
  correct. {a⁺, b⁺, d} independent for d ∈ D; correct. (This is Chvátal–Erdős with κ ≥ 2 ≥ α; the citation
  is attribution only, the proof is self-contained.)
* Lemma 5.2 (shortening, r ≥ 7). The triple i, i+2, i+4 is three distinct vertices because r ≥ 7. Sequence
  1,…,r−6, r−2, r−1, r−5, r−4, r−3, 1: block union = {1,…,r−1} (vertex 0 dropped), joins (r−6)(r−2),
  (r−1)(r−5), (r−3)1 have cyclic differences 4, −4, 4−r ≡ 4. r = 7 instance 1,5,6,2,3,4,1 checked by hand
  (1–5, 6–2, 4–1 are step-4 chords). Verified by script for every r = 7..400 that the sequence is a cycle on
  exactly r−1 vertices using only step-1 and step-4 chords (seatP_work/check_s5.py). CORRECT.
* Lemma 5.3 (size test). Disconnected case and cut-vertex case: correct (in the cut-vertex case |A|+|B| ≥ 2t
  with |A|,|B| ≤ t forces |A| = |B| = t; v misses something in each ⇒ independent triple; else K_{t+1}).
  2-connected requires n ≥ 3: n > k ≥ 5. Shortening needs r ≥ k+2 ≥ 7, i.e. k ≥ 5 — this is where k ≥ 5
  enters, and every later use has k ≥ t ≥ 9 or k ≥ 5. Induced subgraph on a cycle's vertex set has α ≤ 2
  (it is an induced subgraph of H). CORRECT.
  Uses of Lemma 5.3 in §7–§8 (all hypotheses re-checked: k ≥ 5, no C_{k+1}, ω(G) ≤ t, |Y| > max{k,2t}):
  - Lemma 7.3: |B_2| ≥ k+t with t < k ⇒ k+t > k and k+t > 2t. OK.
  - Lemma 8.3: |B_2| ≥ k+1 with k ≥ 2t ⇒ k+1 > k, k+1 > 2t. OK.
  - Prop 8.4, Alt 1 with c ≥ 1: |B_2| ≥ k+3 with k ≥ 2t−2 ⇒ k+3 > k and k+3 ≥ 2t+1 > 2t. OK.
  The intro's "raises the available independence bound from two to three" = Lemma 5.3; it is never applied to
  a set whose size bound was not established first.

### §6 Optimal path systems — checked line by line: CORRECT

* Definition. Paths have distinct endpoints in Q, nonempty interior ⊆ V∖Q, pairwise disjoint interiors,
  distinct represented edges forming a linear forest. Since every interior is nonempty, NO edge of any
  assigned path joins two clique vertices — this is what makes the closing clique edges in Lemma 6.1 new
  edges. (The paper does not say this explicitly; it is immediate. EXPOSITION at most.)
* Lemma 6.1 (closing). u = k+1−q−v; 0 ≤ u ⇔ q ≤ k+1−v; u ≤ t−v ⇔ q ≥ h. Vertex count q+v+u = k+1:
  COUNTED — q interior vertices + v incident clique vertices + u singleton clique vertices, all distinct
  (interiors disjoint and outside Q; clique vertices of different chains distinct). Cycle closure: one list
  path ⇒ it contains an assigned path, ≥ 3 vertices, its two endpoints are distinct clique vertices and the
  closing edge is a clique edge not on the path (previous bullet). ≥ 2 list paths: joining edges are between
  endpoints of different, vertex-disjoint list paths; two-list-path cases (nontrivial + singleton: the two
  joins use the two distinct ends; two nontrivial: four distinct ends; two singletons impossible because
  q ≥ h ≥ 1) checked. Exactly k+1 vertices. CORRECT.
* Existence of the optimum: the empty system is a path system with amount 0 < h (h = k+1−t ≥ 1 since t ≤ k);
  G finite ⇒ finitely many systems ⇒ max L < h exists, then min e. CORRECT. Budget (6.3):
  e ≤ L (amounts ≥ 1), L ≤ h−1 = k−t, |S| = t+L ≤ k. CORRECT.
* Lemma 6.2 (optimality criterion): the three cases A ≥ h (Lemma 6.1), A < h & e' ≥ e (max L),
  A < h & e' < e (max L, then min e). CORRECT. (Note the upper bound A ≤ k+1−v' is only used in case A ≥ h.)
* Lemma 6.3: ≤ |S|−1 neighbours inside S, δ ≥ k ⇒ ≥ k+1−|S| ≥ 1 in F. CORRECT.
* Lemma 6.4. (1) Meeting balls ⇒ x–y walk with ≤ r+s+2 edges, interior outside X, no xy step; the walk visits
  x and y only at its ends (all other vertices are outside X), so shortcutting gives a simple outside path with
  1 ≤ d ≤ r+s+1. Edge between balls ⇒ ≤ r+s+3 edges ⇒ 1 ≤ d ≤ r+s+2. (2) a vertex of B_{r−1}(x) is reached by
  a path of ≤ r edges (take a shortest one in G−X, which is simple and avoids y ∈ X), append y: 1 ≤ d ≤ r.
  CORRECT.
* Cor 6.5 (radius −1 options): mixed case: an edge x–w, w ∈ B_s(y), gives an outside path with
  1 ≤ d ≤ s+1 = r+s+2 internal vertices. CORRECT. (Cor 6.5 is not used in §7–§8; it is used in §9.)
  Computational sanity test of Lemma 5.3 (contrapositive form "α(H) ≤ 2, n > max{k, 2ω(H)}, k ≥ 5 ⇒
  C_{k+1} ⊆ H") over EVERY graph H with α(H) ≤ 2 on 6..11 vertices (complements of all triangle-free graphs from
  nauty-geng): 185,122 (H,k) instances, 0 violations (seatP_work/check_s53.py). Negative control: weakening
  n > 2ω to n ≥ 2ω produces 15 violations already at n ≤ 9 (e.g. 2K_4), so the test can fail.

### §7 Short paths between representatives — checked line by line: CORRECT

* Representatives. ρ(q) = q for chain starts, else the first interior vertex z_1 after the predecessor p.
  Distinctness: each non-start target has its own incoming path, interiors disjoint; starts are clique
  vertices; so |R| = t. CORRECT.
* Lemma 7.1 (replacement). New path q, z_a, …, z_1 = ρ(q), w_1, …, w_d, ρ(q') = z'_1, …, z'_{a'}, q'.
  Simple: the two segments lie in interiors of two DIFFERENT old paths (distinct targets have distinct
  incoming paths) plus their own targets, the w's are in F. Checked the consecutive-on-one-chain case
  p → q → q' explicitly: the segment at q' is z'_1..z'_{a'}, q' and does not contain q. Endpoints q ≠ q' in Q,
  interior nonempty (d ≥ 1) and outside Q. Forest: an oriented chain gives each vertex ≤ 1 incoming edge, so
  after deleting the incoming edges each target has degree ≤ 1; same-chain targets are separated by deleting
  the later target's incoming edge; hence qq' is not an existing represented edge, closes no cycle, creates no
  degree 3. Amount L+d, e+1−r paths: COUNTED. CORRECT.
* Lemma 7.2. Both types give a valid system of amount L+1 with the same or a modified forest. If L+1 = h, the
  new system has v' ≤ t incident vertices, so k+1−v' ≥ k+1−t = h = L+1: it lies in the forbidden interval of
  Lemma 6.1, whose closure has exactly q+v'+u = h+v'+(t−v') = k+1 vertices. CORRECT.
* Degree estimate (display (7.1) after Lemma 7.2): u ∈ B_0(x;S) exists (x has ≥ k neighbours, ≤ |S|−1 ≤ k−1
  in S); u misses R∖{x} by Lemma 7.2; N_F[u] ⊆ B_1(x;S); deg_F(u) ≥ k − (|S| − (t−1)). Improvement by one when
  some y ∈ S∖R is missed by all of B_0(x;S). CORRECT.
* Lemma 7.3. "Every vertex of B_1(x;S) misses R∖{x}": paths x,w,y or x,b,w,y (b ∈ B_0) are simple with 1 or 2
  internal vertices. If B_2 were a clique: |B_1| ≥ k−|S|+t ≥ t forces B_1 = B_2, |B_1| = t, |S| = k; each z
  has ≤ t−1 neighbours in F (all in B_2) and ≤ |S|−(t−1) = k−t+1 in S; δ ≥ k makes both tight, so z is adjacent
  to every vertex of S∖(R∖{x}) ∋ x; B_2 ∪ {x} = K_{t+1}. Contradiction. Second part: I ⊆ B_1 independent pair,
  nonempty; N_G[I] ⊆ S ∪ B_2 with N_G[I] ∩ S ⊆ S∖(R∖{x}); expansion |N_G[I]| ≥ 2k+1 ⇒ |B_2| ≥ 2k−|S|+t ≥ k+t.
  Expansion applied to a genuinely independent nonempty set; subtraction legitimate (B_2 ⊆ F disjoint from S).
  CORRECT.
* Lemma 7.4 (short path, t ≥ 9). Under the negation (no parameter 1..6 between ANY two reps of the fixed
  orientation): Lemma 6.4(1) with r = s = 2 needs exactly 1..6 — matches. 2t > k ⇒ contradiction (α ≤ k).
  2t ≤ k and ⌊k/2⌋ ≤ t ⇒ k ∈ {2t, 2t+1}, t < k. Need two reps with B_1 not a clique; then
  2(t−2)+3·2 = 2t+2 > 2t+1 ≥ k. |S| < k: |B_1| ≥ k−|S|+t > t. |S| = k: L = k−t ≥ t > 0 ⇒ e ≥ 1.
  e ≥ 2: every path is the incoming path of its head target, so ≥ 2 reps are interior vertices; for such x the
  next vertex y toward the target is a later interior vertex or (amount 1) the target, which is not a start and
  hence not in R; consecutive-vertex clause of Lemma 7.2 ⇒ y missed by B_0(x;S) ⇒ |B_1| ≥ t+1. e = 1: reversing
  the single nontrivial chain makes its old end y a representative; y ∉ R; x (a singleton start) is a rep in
  both orientations; Lemma 7.2 in the reversed orientation ⇒ y missed by B_0(x;S). B_1(x;S) does not depend on
  orientation. The negation hypothesis is only used in the ORIGINAL orientation (both for the ball separation
  and for Lemma 7.3's hypothesis at the two chosen x, which are original reps). CORRECT.

### §8 arithmetic — checked by hand AND by script for every t = 9..70, t ≤ k ≤ 2t+1 (seatP_work/check_s8_arith.py/.out)

* Lemma 8.1's "all selected amounts ≥ j+2" contradiction: f(j) = (t−j−1)(j+2) is concave; f(1) = 3t−6,
  f(5) = 7t−42; margins over 2t+2 are t−8 and 5t−44, both ≥ 1 at t = 9 (interior values at t = 9: 24, 25, 24
  vs 20). Script: 0 solutions of {2r ≥ t−j+1, (r−1)(j+2) ≤ k−t} for t = 9..70. CONTROL: at t = 8 solutions
  exist (e.g. t=8, k=15, j=5, r=2), i.e. this is exactly where the t ≥ 9 hypothesis is consumed and why t ≤ 8
  must go to §9.
* Lemma 8.2's classification: enumerated every (t,k,d,e,v,a) satisfying the constraints the proof derives
  (2 ≤ d ≤ 6, de ≤ L = k−t, e+1 ≤ v ≤ 2e or e = v = 0, a ≤ min{2, t−v}, v+a ≥ t−d+2): every survivor is in one
  of the three alternatives, with the stated endpoint restriction; Alt 2 survivors exactly (t,k,e,v,a) =
  (9,18,3,6,2), (9,19,3,6,2), (11,23,4,8,2); Alt 3 exactly (9,19,2,4,2). Note Alt 2 at t = 9 allows k ∈ {18,19}
  (the lemma does not claim otherwise). The per-d hand computations (d=3: t ≤ 11, t = 10 dies on
  3⌈7/2⌉ = 12 > 11; d=4: t ≤ 9, 4⌈5/2⌉ = 12 > 10; d=5: 3t ≤ 27; d=6: 4t ≤ 38, 6⌈3/2⌉ = 12 > 10) all re-done: correct.
* Lemma 8.3 one-chain bound ⌊(t+1)/2⌋+1 < t−2 holds for all t ≥ 9 (t = 9: 6 < 7).
* Prop 8.4 final counts: Alt 1, c ≥ 1: 3(t−c) ≥ 3t−6 > 2t+1 ≥ k (needs t ≥ 8); Alt 1, c = 0: 3(t−1) > 2t+1;
  Alt 2: 3(t−2) > 2t+1; Alt 3: 4·3+5·2 = 22 > 19. Script: 0 failures.

### §8 Excluding large cliques — checked line by line: CORRECT

* Lemma 8.1. "If L+d < h, then R contradicts the maximality of L" — yes (L < L+d < h). Otherwise the
  inclusion-minimal subcollection X of R with amount ≥ h exists (R itself qualifies) and is a valid path system
  (any subcollection of a path system is one: sub-forest of a linear forest, distinct edges, disjoint interiors).
  It contains the new path (old paths total ≤ L < h). 0 ≤ j ≤ 5 from h+j ≤ L+d ≤ h+5. Lemma 6.1 ⇒ w > t−j ⇒ j ≥ 1;
  2r ≥ w. Minimality ⇒ every selected amount ≥ j+1. The "all ≥ j+2" branch: (r−1)(j+2) ≤ L (only the r−1 old
  selected paths are used), 2(r−1) ≥ t−j−1 — arithmetic re-done above. A selected path of amount exactly j+1
  deleted ⇒ valid system of amount h−1 ⇒ L = h−1 (L ≤ h−1 always); it has r−1 paths and amount L ⇒ r−1 ≥ e by the
  tie-break; |R| ≤ e+1 ⇒ X = R ⊇ P. j = d−1 by comparing amounts; new path amount = (L+d) − L = d; every selected
  (hence every old) amount ≥ j+1 = d. CORRECT. (The tie-break is genuinely needed here: without "fewest paths" the
  step r−1 ≥ e fails. The paper uses it correctly.)
* Lemma 8.2. Lemma 7.1's system consists of unchanged old paths + one new path, amount L+d ⇒ Lemma 8.1 applies ⇒
  r = 0 ⇒ both targets are chain starts; every old amount ≥ d; j = d−1 ≥ 1 ⇒ d ≥ 2 (consistent with Lemma 7.2).
  Incident count of the new system is v+a (non-missing starts were already incident; missing ones become
  incident) — COUNTED. Amount h+d−1 ≥ h, so Lemma 6.1 forbids v+a ≤ t−d+1 ⇒ (8.2) v+a ≥ t−d+2. Then (8.3) and the
  case analysis — re-done (above). "Mutually exclusive properties of the fixed old system" (v ≥ t−2 / v = t−3 /
  t = 9, v = t−5 = 4) do not depend on the orientation or the pair, so the final paragraph's "applies to every
  outside path ... in every orientation" is justified: any second short path would itself force an alternative,
  necessarily the same one, with its own parameter and endpoint restriction. CORRECT.
* Lemma 8.3. ≥ 2 nonsingleton chains: Alt 2 matching of 3 or 4 edges, Alt 3 of 2 edges, Alt 1 via
  e+1 ≤ ⌊(t+1)/2⌋+1 < t−2 (uses 2e ≤ L ≤ t+1 from amounts ≥ 2). Reversal trick: the reversed chain is not the
  chain of x's target, so x stays a representative; its old terminal vertex y is a clique vertex of another chain,
  hence y ≠ x and y ∉ R (it had an incoming path). Lemma 7.2 in the original orientation excludes R∖{x}, in the
  reversed orientation excludes y: t excluded vertices of S, so N[z] ∩ S has ≤ |S|−t elements for z ∈ B_0(x;S);
  N[z] ⊆ S ∪ B_1(x;S); |S| = k because L = k−t (Lemma 8.2). |B_1| ≥ t+1 ⇒ independent pair I (ω = t);
  N[I] ⊆ S ∪ B_2 ⇒ |B_2| ≥ 2k+1−k = k+1 > max{k,2t} when k ≥ 2t. CORRECT.
* Prop 8.4.
  - Alt 1, c ≥ 1: all chosen targets are incident, so no pair's union contains a missing vertex ⇒ parameters 1..6
    forbidden (Lemma 8.2's last paragraph) ⇒ radius-2 balls separated (Lemma 6.4(1), r = s = 2 needs 1..6).
    k = t+L ≥ t+2e ≥ t+v ≥ 2t−2. Triple claim: Lemma 6.4(2) with r = 2 (parameters 1,2 forbidden) ⇒ each of ≥ 2
    other chosen reps y has no neighbour in B_1(x;S); I ⊆ B_1(x;S) independent pair from Lemma 8.3; N[I] ∩ S
    misses those two y ⇒ |B_2| ≥ 2k+1−(k−2) = k+3 ≥ 2t+1. Size test hypotheses met. Count 3(t−c) ≥ 3t−6 > 2t+1.
    CORRECT. (The argument actually excludes v−1 ≥ t−3 vertices, more than needed.)
  - Alt 1, c = 0: e = ⌈t/2⌉, k ≥ 2t. Even t: matching, at most one amount 3 (L ≤ 2e+1). Odd t: L = t+1, all
    amounts 2, v−e = e−1 chains carrying e edges ⇒ exactly one 2-edge chain. Chosen-vertex counts t or t−1 (even),
    2+2(e−2) = t−1 (odd) — COUNTED. Separation: pairs on different chains / the two forward reps of the 2-edge
    chain are simultaneous reps whose targets both have incoming paths ⇒ Lemma 7.1's system removes an old path ⇒
    Lemma 8.1 forbids d = 1..6; the pair a,b of one amount-two path u,a,b,v: replacing the step ab by the outside
    path gives a system with e−1 old paths + a new u–v path of amount 2+d, total L+d ⇒ Lemma 8.1 forbids it
    (it does not contain all e old paths). Every pair of chosen vertices falls in one of these cases (checked;
    in the even case the amount-3 path contributes only one vertex). Count 3(t−1) > 2t+1. CORRECT.
  - Alt 2: k ≥ (5t−9)/2 ≥ 2t (t ≥ 9). Bases: reps of the t−3 incident targets (half of them are clique vertices,
    the chain starts of the matching edges — allowed: Lemma 8.3 covers every representative) + one missing target.
    No pair has two missing targets ⇒ 1..6 forbidden. 3(t−2) > 2t+1. CORRECT.
  - Alt 3: radius pairs (2,2),(2,1),(1,1) need 1..6, 1..5, 1..4 forbidden; the only permitted parameter is 5 and
    only for missing–missing pairs, and missing–missing needs only 1..4. 4·3+5·2 = 22 > 19 (Lemma 8.3 gives α ≥ 3 in
    B_2 because 19 ≥ 18 and α ≥ 2 in B_1). CORRECT.

### "Immediate / the same argument / directly" steps in §5–§8 — every one re-done explicitly
* §5, Lemma 5.3: "the same argument shows that H−v has exactly two components" — H−v is an induced subgraph
  (α ≤ 2) and disconnected (v a cutvertex); three components or a non-edge inside one component plus a vertex of
  another give an independent triple. Correct as stated.
* §6, Lemma 6.1: "All remaining cases follow directly from vertex-disjointness" — ≥ 3 list paths, or two
  nontrivial ones: the joining clique edges join endpoints of distinct vertex-disjoint paths and are pairwise
  distinct (they have distinct end-sets); none lies on a list path (no assigned path contains a clique–clique
  edge). Correct.
* §6, Cor 6.5: "The case of two singletons is immediate" — {x},{y} with x ≠ y, xy ∉ E. Correct.
* §7, Lemma 7.1: "If they belonged to different chains, this is immediate" — deleting edges cannot merge
  components. Correct.
* §7 after (7.1): "the same count improves the right-hand side by one" — u's S-neighbours avoid
  (R∖{x}) ∪ {y}, a set of t vertices of S∖{x}. Correct.

### Citations used in §5–§8 (and the Pósa citation in §3)
* §5 cites Chvátal–Erdős 1972 Thm 1 (κ ≥ α ⇒ Hamiltonian; the 2-connected/α ≤ 2 case is indeed a special case)
  and Radziszowski–Jin 1994 Thm 2 for the shortening idea. Both are attribution only: complete proofs are given
  (Lemmas 5.1, 5.2) and I checked those proofs, so neither citation is load-bearing.
* §6–§8 cite nothing external.
* Pósa 1963 is cited only in §3 ("We use the standard fixed-end path rotation of Pósa [p. 358]"). I rendered
  p. 358 of the primary scan (real.mtak.hu, fetched into seatP_work/dl_posa/): it contains exactly the rotation
  "(a_{i_k−1} … a_2 a_1 a_{i_k} … a_m) has the same length as P" for an edge from the end a_1 to a_{i_k}. The paper
  then re-derives the rotation it uses (display after the citation: v_1,…,v_j,v_r,v_{r−1},…,v_{j+1}). So the
  citation says what is claimed and is in any case not load-bearing. (§3 itself was refereed by the main seat.)

### Exhaustive abstract model check of §7.1/§8 (seatP_work/model_s8.py; outputs model_t10..12.out, t = 9 in altcount_t9.out — same program plus a branch tally)

Independent code (own pattern generator, own construction of replacement systems). Only source of contradiction:
Lemma 6.2's window "L + 1[e' ≥ e] ≤ A ≤ k+1−v'" applied to EVERY sub-collection of the modified system (this is
all that Lemmas 8.1/8.2 use). For every t ∈ {9,10,11,(12)}, every k ∈ [t, 2t+1], every weighted linear forest P on t
clique vertices with L ≤ k−t, every pair of targets, every orientation of their chains and every d ∈ {1..6}, it
builds Lemma 7.1's system and decides whether it is forbidden; it also tries every "replace one step of one old
path by a d-detour" system (the construction of Prop 8.4, Alt 1, c = 0, and of Lemma 7.2's second clause). Checks:
(i) every non-forbidden Lemma-7.1 system removes no old path, has L = k−t, d ≥ 2, all old amounts ≥ d, and falls in
exactly the alternative of Lemma 8.2 with its endpoint restriction; (ii) every step-detour system is forbidden;
(iii) Lemma 8.3's "≥ 2 nonsingleton chains" for every pattern admitting a survivor; (iv) for every such pattern,
builds Prop 8.4's chosen bases/radii exactly as printed and verifies that each pair's required parameter range
(1..r+s+2) is forbidden by some construction, and that the independence total exceeds k.

| t | (pattern,k) instances | Lemma-7.1 systems | non-forbidden | step-detours | non-forbidden | bad | sep. fail | count fail | patterns reaching §8.4 |
|---|---|---|---|---|---|---|---|---|---|
| 9  | 4,158  | 2,269,614  | 94  | 118,680 | 0 | 0 | 0 | 0 | 20 |
| 10 | 9,623  | 6,649,626  | 118 | 309,900 | 0 | 0 | 0 | 0 | 19 |
| 11 | 21,966 | 18,663,840 | 110 | 786,318 | 0 | 0 | 0 | 0 | 19 |
| 12 | 50,021 | 51,309,036 | 164 | 1,970,364 | 0 | 0 | 0 | 0 | 19 |

Every branch of Prop 8.4 is exercised (so the packing checks are not vacuous): t = 9 → Alt 1 with c = 2 (10
patterns), c = 1 (6), c = 0 (1, odd t), Alt 2 (2), Alt 3 (1); t = 10 → Alt 1 with c = 2 (14), c = 1 (3), c = 0 (2,
even t) (seatP_work/altcount_t9.out, altcount_t10.out). Alt 2 at t = 11 occurs in the t = 11 run (k = 23).

POSITIVE CONTROL (the instrument can fail): the same program at t = 8 reports 169 "bad" survivors (Lemma-7.1
systems that remove an old path yet are not forbidden, e.g. P = ((),(),(),(),(1,),(8,)) at k = 17), 3 non-forbidden
step-detours, and patterns with no alternative / one nonsingleton chain — i.e. it detects exactly that Lemma 8.1
fails below t = 9, which is why t ≤ 8 is handed to §9.

### What §8 hands to §9, and whether §9.1 covers it (brief item 3) — CLEAN HAND-OFF

§8 side (quoted): "Proposition 8.4. There is no counterexample G with maximum clique size t ≥ 9." Assembled in the
proof of Theorem 1.1 (§9.6): "Theorem 3.1 gives max{3,⌊k/2⌋} ≤ t = ω(G) ≤ k. Proposition 4.1 rules out k = 3,4.
For k ≥ 5, Proposition 8.4 rules out t ≥ 9. The remaining values satisfy (9.1), so Proposition 9.1 rules them out
as well."

§9 side (quoted): "(9.1) 5 ≤ k ≤ 17, max{3,⌊k/2⌋} ≤ t ≤ min{8,k}." Prop 9.1: "... every optimal path system on a
maximum clique, chosen as in Section 6, gives a contradiction under these hypotheses." Lemma 9.2: the lists
"represent exactly once the isomorphism classes of linear forests on t vertices with positive integer edge amounts
of total at most B", with B = k − t (Table 1 caption), and "Unused amount budget is allowed: optimality does not
require L = k−t".

Assessment:
* The arithmetic of the hand-off is right: k ≥ 5 and t ≤ 8 with ⌊k/2⌋ ≤ t ⇒ k ≤ 17; t ≥ 9 is impossible for k ≤ 8
  (t ≤ k). Every (k ≥ 5, t) with max{3,⌊k/2⌋} ≤ t ≤ k is either t ≥ 9 (Prop 8.4) or in (9.1).
* §8 does NOT hand §9 a restricted family of "configurations left open" (none of Lemmas 7.x/8.x is cited in §9 —
  checked by grepping every \ref in 09-*.tex/10-*.tex: §9 cites only Lemma 2.2, Thm 3.1, Lemma 5.3, Lemma 6.1,
  Lemma 6.4, §6 and Prop 4.1/8.4 in the final assembly). §9 restarts from the §6 optimal system for each (k,t) in
  (9.1), and Lemma 9.2 enumerates EVERY weighted linear forest with L ≤ k−t. Every optimal system satisfies
  L ≤ k−t by (6.3) and has a linear forest with ≤ t−1 edges on Q, so it is in the list. Coverage is therefore
  complete by construction, not by matching §8's alternatives.
* Prop 9.1's hypotheses are weaker than the §2 setting (no |V(G)| = ka+1, α ≤ k instead of α ≤ a, and the
  clique range is a hypothesis instead of Theorem 3.1's conclusion). That is fine: §6's construction and the
  facts §9 imports (δ ≥ k from expansion; Lemmas 5.3, 6.1, 6.4) use only no-C_{k+1}, ω = t, α ≤ k, expansion.
  The minimal counterexample satisfies all of them (Lemma 2.2 + Thm 3.1).
* Independent recount of Table 1 with my own generator (seatP_work/count_patterns.py/.out): 42 parameter pairs,
  3,099 patterns, every per-(k,t) count equal to Table 1. The generator itself was cross-checked against a brute-force
  enumeration of all labelled weighted linear forests (edge subsets of K_t × amount assignments, canonicalised) for
  (t,B) = (3,2),(4,2),(5,2),(4,4),(5,3),(6,2),(5,5),(6,3): identical counts. So Lemma 9.2's coverage and the 3,099
  figure are confirmed independently. (Whether each of the 3,099 patterns is actually refuted is §9.2–§9.6 + the
  verifier's business, not this seat's.)

### Objections (all EXPOSITION; no FATAL, no GAP found)

E1 (EXPOSITION, Lemma 6.1). "If there is only one path in the resulting list ... The clique edge between its
distinct endpoints closes it into a simple cycle." The reason the closing (and, later, joining) clique edges are not
already edges of the expanded paths — every assigned path has nonempty interior, so no assigned path contains a
Q–Q edge — is not stated. One sentence fixes it.

E2 (EXPOSITION, notation). Symbols are reused with different meanings inside §7–§8: `a` = interior count in the
definition of ρ ("p, z_1, …, z_a, q, a ≥ 1"), = number of missing targets in Lemma 8.2 ("Let a ∈ {0,1,2} be the
number of missing targets"), = an interior vertex in Prop 8.4 ("interior vertices a,b of a single amount-two path
u,a,b,v"); `v` = incident-vertex count and also a clique endpoint in that same sentence ("u,a,b,v"); `r` = radius
(§6), number of deleted incoming paths (Lemma 7.1), number of selected paths (Lemma 8.1). No step is wrong because
of it, but "u,a,b,v" right after "v ≥ t−2" is a trap for a reader.

E3 (EXPOSITION, Lemma 8.2 proof). "The proof of Lemma 8.1 also gives j = d−1 ≥ 1, so d ≥ 2." This leans on an
internal step of another proof, not on the statement of Lemma 8.1. Harmless (d ≥ 2 for rep-to-rep paths is also
Lemma 7.2), but the cleaner fix is to add "and d ≥ 2" to the statement of Lemma 8.1, which the proof does establish
(j ≥ 1 and j = d−1).

E4 (EXPOSITION, Lemma 8.1). "a valid path system consisting of some paths of P and one new path" — "new" should
be read as "not a path of P" (in both applications the new path contains vertices of F, so this holds). Worth
saying.

E5 (EXPOSITION, Lemma 7.4 statement). Proved "for every fixed orientation"; only existence for one orientation is
used in Prop 8.4. Fine as is.

Things I specifically tried to break and could not:
* Whether Lemma 8.1's tie-break step (r−1 ≥ e) silently needs a different optimality notion than §6's — it does
  not; §6 chooses min e among amount-L systems, which is exactly what is used.
* Whether Lemma 8.3's reversal could make y = x or y ∈ R (it cannot: y is a clique vertex of a different
  nonsingleton chain, with an incoming path in the original orientation).
* Whether Alt 1 (c ≥ 1) of Prop 8.4 needs k ≥ 2t for its triples (it does not; it gets |B_2| ≥ k+3 from two
  extra excluded representatives, valid since k ≥ 2t−2).
* Whether Alt 2's bases include clique vertices whose balls are not covered by Lemma 8.3 (they are covered: the
  lemma is stated for every representative, and chain starts are representatives).
* Whether a pair of chosen bases in Alt 1, c = 0 escapes both of the paper's two separation arguments (checked by
  hand and by the model check: every pair is either a simultaneous-representative pair with two incoming paths or
  the two interior vertices of one amount-two path).
* Whether any "forbidden improvement" breaks the path-system side conditions or is closed to a cycle of the wrong
  order: every closure goes through Lemma 6.1, whose vertex count q+v+u = k+1 I counted; every improvement was
  re-checked for interior-disjointness, distinct represented edges and linear-forest structure.

### Limits of this seat's checking (so nobody over-reads the green)
* The model check works at the path-system level only (forest + amounts, contradictions from Lemma 6.2). The
  graph-level steps — ball growth (7.1)/(7.2), Lemma 7.3's clique case, Lemma 8.3's |B_1| ≥ t+1 and |B_2| ≥ k+1,
  the per-ball triples via Lemma 5.3, Lemma 6.4's separation — are checked by hand only (they are short and I
  re-derived each). The per-ball independence values the model check adds up (3 for radius 2, 2 for radius 1) are
  the paper's, taken from those hand-checked lemmas.
* The model check covers t = 9..12; for larger t the proofs of Lemmas 8.1–8.2 are uniform inequalities whose
  arithmetic I brute-forced for t ≤ 70 and which are linear/concave in t beyond that.
* I did not referee §9.2–§9.6, Appendix A, the verifier, or the Lean development.
