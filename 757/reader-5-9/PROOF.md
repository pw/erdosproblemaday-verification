# Erdős #757 — reader submission 7bkzb8: c* ≤ 5/9

Problem (erdosproblems.com/757; Formal Conjectures `erdos_757`): a finite A ⊂ ℝ is a (4,5)-set if every
4-subset B has |B − B| ≥ 11 (≥ 5 distinct positive differences). h(A) = largest Sidon subset (all sums a+b,
a ≤ b, distinct — so 3-APs are forbidden). c* = best constant with h(A) ≥ c*|A| for every (4,5)-set A.
Known: 9/17 ≤ c* ≤ 4/7 (Ma–Tang, arXiv:2602.23282 v2; 4/7 from a 14-point set with h = 8).
Ma–Tang Thm 1.5: c* = inf_n f(n)/n, f(n) = min h over (4,5)-sets of size n. (Not even needed for an upper
bound: any single (4,5)-set A gives c* ≤ h(A)/|A| directly from the definition.)

## The submission (verbatim construction)
O = {0,49,75,83,98,101,117,119,121,159,269}, φ(x) = 101 + 18x/269 (so φ(0)=101, φ(269)=119 ∈ O).
S_K = O ∪ φ(O) ∪ … ∪ φ^K(O). Claim: S_K is a (4,5)-set, |S_K| = 11+9K, h(S_K) = 7+5K, hence
c* ≤ lim (7+5K)/(11+9K) = 5/9.

## Theorem (what we verify)
For every K ≥ 0: |S_K| = 11+9K, S_K is a (4,5)-set, and h(S_K) = 7+5K exactly. Consequently
c* ≤ (7+5K)/(11+9K) for every K, so c* ≤ 5/9. Already K = 6 (65 points, h = 37) gives 37/65 < 4/7.

## Proof

**P1 (O, computed).** The additive relations of O (a+b=c+d, {a,b}≠{c,d}, a=b allowed) are exactly nine 3-APs:
{0,49,98} {49,75,101} {49,83,117} {49,159,269} {75,98,121} {75,117,159} {83,101,119} {83,121,159} {117,119,121}.
No 4-point relation. O is a (4,5)-set; h(O) = 7. (9 = |O| − 2, the maximum allowed by Ma–Tang Lemma 2.4.)

**P2 (coordinates).** L = 101·269/251 = 27169/251 is the fixed point of φ; φ(x) − L = r(x − L), r = 18/269.
Every point of S_K has a unique canonical form p = φ^j(x) with either j = 0, x ∈ O, or 1 ≤ j ≤ K,
x ∈ O \ {0,269} (because φ^j(0) = φ^{j−1}(101), φ^j(269) = φ^{j−1}(119)). Call j the level. Then
251(p − L) = r^j z(x) with z(x) = 251x − 27169 (nonzero integers; |z(x)| ≤ 14870 for x ∈ O\{0,269}).
Note 27169 = 101·269, so z(x) ≡ 251x (mod 269).
*Uniqueness (fills referee gap a).* If φ^j(x) = φ^{j'}(x') with canonical forms and j < j', then
r^j z(x) = r^{j'} z(x'), i.e. 269^{j'−j} z(x) = 18^{j'−j} z(x'); mod 269 this forces 269 | z(x'), i.e. 269 | x',
impossible for x' ∈ O\{0,269} (and j' ≥ 1). If j = j' then z(x) = z(x'), so x = x'. Hence |S_K| = 11 + 9K
(11 points at level 0, 9 at each level 1..K), and copy i = φ^i(O) consists of the 9 level-i points φ^i(x),
x ∈ O\{0,269}, plus φ^i(0) = φ^{i−1}(101), φ^i(269) = φ^{i−1}(119) at level i−1 (copy 0 = the level-0 points).
So copies i < j meet only if j = i+1, and then in exactly {φ^i(101), φ^i(119)}; all other pairs are disjoint.

A nontrivial relation Σ ε_i p_i = 0 (Σ ε_i = 0; either 4 distinct points with ε = ±1, or 3 points with
coefficients 1,1,−2) is equivalent to Σ ε_i r^{j_i} z(x_i) = 0.

**P3 (span lemma).** Any nontrivial relation among points of any S_K has max level − min level ≤ 10.
Let J = max level, m = min level, J > m (else: all points at one level j; if j = 0 they lie in O = copy 0,
if j ≥ 1 they are φ^j(x), x ∈ O, i.e. in copy j).
- Top: multiply by 269^J and reduce mod 269: Σ_{top} ε_i x_i ≡ 0 (mod 269). A single top point (coefficient
  ±1 or ±2) would need 269 | x with x ∈ O\{0,269} ⊂ [49,159] — impossible. So ≥ 2 distinct points at level J.
- Any two distinct points at one level have T = ε1 z1 + ε2 z2 ≠ 0 with ε ∈ {±1, ±2}: z1 = −z2 would need
  x1+x2 = 2L ∉ ℤ; z1 = z2 means the same point; z1 = ±2 z2 would need 251 | 27169 or 251 | 81507, and neither
  holds (fills referee gap b; exhaustive check over all ordered pairs of O agrees). Hence for every group G of
  ≤ 2 points at one level, Σ_G ε z ≠ 0.
- Level patterns (top first): 3 points: (2,1); 4 points: (3,1), (2,2), (2,1,1).
- Two levels, gap d = J − m: B + r^d T = 0, B = bottom sum ≠ 0 integer, |T| ≤ 3·14870 (top weight ≤ 3, top
  points have level ≥ 1). So 1 ≤ 44610 r^d ⇒ d ≤ 3. (Sharper, from the referee: 269^d B = −18^d T forces
  269^d | T, and 0 < |T| ≤ 44610 < 269², so d ≤ 1.)
- Three levels (2,1,1), gaps g1 (bottom→middle), g2 (middle→top):
  ε_b z_b + ε_c r^{g1} z_c + r^{g1+g2} T = 0. With |z_b| ≥ 1: 1 ≤ r^{g1}(14870 + 2·14870 r) ⇒ g1 ≤ 3.
  Dividing by r^{g1}: N/18^{g1} = −r^{g2} T with N = ε_b z_b 269^{g1} + ε_c z_c 18^{g1} ∈ ℤ, N ≠ 0 since T ≠ 0.
  So r^{g2}·29740 ≥ 18^{−3} ⇒ g2 ≤ 7. Span ≤ 10.

**P4 (computation + shift).** (Independent referee brute force: exactly 9(K+1) relations, none 4-point, none
crossing copies, for K up to 150.) If Σ ε_i r^{j_i} z_i = 0 then Σ ε_i r^{j_i − m} z_i = 0: shifting all levels down by m
gives a nontrivial relation among canonical points of S_{J−m} (level-0 points need only x ∈ O). Exhaustive
enumeration (`relations.py`, exact rationals) shows every relation of S_12 lies inside a single copy φ^t(O)
(117 = 9·13 relations, 0 cross-copy; an injected cross-copy point is detected). By P3 every relation of every
S_K is a level-shift of a relation of S_10 ⊂ S_12, hence lies inside a single copy (copy t+m). In particular every
relation of S_K is one of the 9(K+1) images φ^t of O's 3-APs.

**P5 ((4,5) for all K).** Coincidences among B's six differences are relations among B's points. For
a < b < c < d the only 4-point relation is a+d = b+c, which makes exactly two equalities (b−a = d−c and
c−a = d−b); a 3-AP makes exactly one. |B−B| < 11 means at most 4 distinct positive differences among 6, i.e.
(with s_k the multiplicities) Σ(s_k − 1) ≥ 2, so at least two equal pairs of differences (fills referee gap c). Let B ⊆ S_K, |B| = 4, with ≥ 2 coincidences. If B lies in one copy,
contradiction (copy ≅ O is (4,5)). Otherwise every relation of B lies in a copy and so is a 3-AP; two distinct
3-APs in B share 2 points; they are not in the same copy (else B ⊆ that copy); copies φ^i(O), φ^j(O) intersect
only when |i−j| = 1, in exactly {φ^i(101), φ^i(119)} = {φ^{i+1}(0), φ^{i+1}(269)}. So both APs contain both shared
points: in copy i+1 that is a 3-AP of O containing 0 and 269 — none exists. Contradiction. (Also checked directly
for K ≤ 12 by the literal |B−B| ≥ 11 test, `check45.py`.)

**P6 (h exactly).** By P4, T ⊆ S_K is Sidon iff T contains none of the 9(K+1) copy-APs. Chain DP over the overlap
pairs (`transfer.py`): copy-0 vector (by T ∩ {101,119}) = [6,7,7,7]; transfer M[L][R] (L = T ∩ {0,269} of the new
copy, R = T ∩ {101,119}; value = |T| − |L|) = rows [5,6,6,6],[4,5,5,5],[4,5,5,5],[4,5,5,5]. One step maps
[6,7,7,7] ↦ [11,12,12,12] = [6,7,7,7] + 5, so by max-plus linearity v_K = [6+5K, 7+5K, 7+5K, 7+5K] for all K and
h(S_K) = 7 + 5K. Cross-checks: CP-SAT (K ≤ 8, OPTIMAL) and CaDiCaL + sequential-counter cardinality on a separately
written integer construction with a distance-collision encoding (K ≤ 8: ≥ 7+5K SAT, ≥ 8+5K UNSAT).

Hence c* ≤ inf_K (7+5K)/(11+9K) = 5/9 (the infimum is the limit; not attained). Improves Ma–Tang's 4/7.
