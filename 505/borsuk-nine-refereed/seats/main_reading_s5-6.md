# Main seat — line-by-line reading of §§5–6 (printed numbering), 2026-10-20 ~18:20Z
Reader: the 18:00Z erdos cron seat (Claude Opus 5.5) itself, from /tmp/oaimath/156/paper.txt (pdftotext -layout), before any referee report
came back. Verdict: **HOLDS AS READ.** No gap; no exposition finding beyond seat T's. Each step below was checked by hand; Lemma 5.3 also by
exhaustive computation (`finite/triangle_systems.py`).

## Lemma 5.2 (admissible RP² → Δ⁵ gives a six-label triangle system)
- Pure 2-dim, all 15 edges, each edge in a positive even number of triangles: Theorem 4.3 (k = 3) + Prop 4.1. ✓
- Complementary triples not both triangles: witness lines x, y; a line ⊥ both exists in ℝ³; its support would avoid all six labels. ✓
- ≤ 10 triangles (one per complementary pair) and ≥ 2·15/3 = 10 (each edge ≥ 2, 3 edges per triangle) ⇒ exactly one per pair, each edge exactly 2. ✓

## Lemma 5.3
- (1) link at a: every vertex degree 2 (pair {a,u} in exactly two triangles) on 5 vertices ⇒ a 5-cycle (no 3+2 split). ✓
- (2) α(C₅) = 2 ⇒ any three of A∖{a} contain a link edge ⇒ a triangle in A; all four triples would put a 3-cycle in a 5-cycle. ✓
- (3) with {a,b,c},{a,b,d} the triangles on {a,b}: deleting b from the link at a leaves a path c…d with middle edge {e,f}, so the outer edges
  are M1 = {ce, df} or M2 = {cf, de}; same for the link at b; if a's path uses M1 then {a,c,e},{a,d,f} ∈ T exclude {b,d,f},{b,c,e}, so b's
  path uses M2. Symmetric difference of the two paths = the 4-cycle M1 ∪ M2; every 3 of its 4 vertices keep an edge ⇒ the restrictions to
  any R differ ⇒ no transposition (a b) preserves T. ✓
- (4) a triple through the omitted vertex z has its complement inside the 5-set; the complementary-triple rule decides it. ✓
- Exhaustive: exactly 12 systems, one S₆-orbit, |Aut| = 60, no transposition; (1)–(4) hold on all 12; the hemi-icosahedron's 10 faces are one
  of them (the identification with the six-vertex ℝP² is ours; §5 never names it).

## Lemma 6.1
- Witness x with S(x) = S (S is a facet: Theorem 4.3 gives facets of size 4, so no 5-face). f on P(x⊥) ≅ RP² uses only labels of C = [10]∖S,
  and all six (else < N₃ = 6 labels, contradicting Prop 4.1 in ℝ³) ⇒ Lemma 5.2 applies. ✓
- No extra triangles on C: an extra T ⊂ C has C∖T in the system ⇒ both triangles of K; witness lines for S, T, C∖T and a line ⊥ all three in ℝ⁴
  ⇒ that line has no admissible label. ✓  Disjoint tetrahedra ⇒ four triples of one 4-set in a system, contra 5.3(2). ✓

## Lemma 6.2 (every triangle in exactly two tetrahedra)
- Transport: tetrahedra differing by a ↔ b have complements C₁ ∋ b, C₂ ∋ a sharing 5 labels; (a b) fixes the shared 5-set pointwise and carries
  T_{C₁} to a system agreeing with T_{C₂} there ⇒ equal by 5.3(4). ✓
- Three tetrahedra T∪{a}, T∪{b}, T∪{c}: complements R∪{b,c}, R∪{a,c}, R∪{a,b}, |R| = 4; transports (a b), (b c), (c a); composite: a↦a,
  b↦c, c↦b, i.e. (b c), fixing R and preserving T_{R∪{b,c}} — contra 5.3(3). ⇒ ≤ 2; positive even ⇒ exactly 2. ✓

## Lemma 6.3 (edge links are 3- or 4-cycles)
- Degree 2 by 6.2. A 5-vertex path v0..v4, R = the 3 labels outside D ∪ {v0..v4}; tetrahedra D∪{v_i,v_{i+1}}; consecutive complements
  differ by (v0 v2), (v1 v3), (v2 v4); composite sends v4 ↦ v2 and fixes R (tracked by hand). {v2,r,s} lies in both end complements, so its
  membership is membership in K ⇒ links at v4 and v2 in T₁ agree on R — contra 5.3(3). ✓

## Lemma 6.4 (partner blocks)
- p(v) unique and outside S (6.2 on S∖{v}; the only tetrahedron on S's vertices is S). Blocks B_y = p⁻¹(y) ∪ {y} disjoint, size ≥ 2. ✓
- Exchange v → a = p(v), S' = (S∖v) ∪ {a}: p'(a) = v. For w ≠ v, D = S∖{v,w}, b = p(w): link of D has edges {v,w}, {w,a}, {v,b}.
  a = b ⇒ a 3-cycle component ⇒ other tetrahedron on D∪{a} is D∪{a,v} ⇒ p'(w) = v. a ≠ b ⇒ path a–w–v–b on 4 distinct vertices ⇒ by 6.3
  a 4-cycle closing with {a,b} ⇒ p'(w) = b. Hence block B_a is re-indexed by v with the same elements; others unchanged. ✓
- Any omission pattern is reached by one exchange per block (replace present u by its partner q); Σ(|B_y| − 1) = 4. ✓
- A tetrahedron meeting each block in ≤ 1 element is disjoint from the tetrahedron omitting those elements ⇒ contra 6.1. ✓

## Theorem 6.5
- t blocks hold 4 + t labels; |R| = 6 − t, 1 ≤ t ≤ 4. t = 4 ⇒ all blocks of size 2 and S meets each once — contra 6.4's last clause. ✓
- No triangle inside R (its extension would have ≤ 1 block vertex); every 4 labels of [10]∖S ⊇ R contain a triangle (6.1 + 5.3(2)) ⇒ |R| ≤ 3
  ⇒ t = 3, |R| = 3, sizes 3, 2, 2. ✓
- Complement of S = R ∪ {q₁,q₂,q₃}; for r, s ∈ R the two triangles on {r,s} have third vertices among the q's, distinct; only one block has
  size 3 ⇒ some {r,s,z} with z in a 2-block B; a tetrahedron on it needs two vertices of one block, which can only be z and the other
  element of B ⇒ at most one tetrahedron — contra 6.2. ✓

Independent cross-check of the CONCLUSION (not of these steps): `finite/` SAT encoding, UNSAT with cake_lpr-verified certificates.
