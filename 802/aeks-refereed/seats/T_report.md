# Seat T report — §§3–5 (Theorem 3.1: triangle mass from cross mass)

VERDICT: HOLDS AS READ — every displayed identity and inequality in §3 (Thm 3.1 statement, Lemma 3.2, Lemma 3.3),
§4 (Lemma 4.1) and §5 (Lemmas 5.1–5.3, Prop 5.4, proof of Thm 3.1, (5.10)) re-derived by hand with the printed
constants; no FATAL item and no GAP found. Five EXPOSITION-level notes (E1–E5 below), none affecting any constant.
Numerics: every mechanical identity checked on random weighted graphs to ~1e-15; every displayed inequality held;
negative controls confirm each instrument can fail. No counterexample to any displayed identity.

Reader: seat T (hostile). Source: the .tex for printed §3 (invariant.tex), §4 (entropy.tex), §5 (coupling.tex), §2 for
the definitions of e_w and g_x, §6 for the use of (5.10). Cross-checked against indep.txt (PDF text): constants agree —
E_C = 42C^2+2C, A_C = 10+E_C, B_C = 2sqrt(A_C+1), R = ceil(x), delta_x = (A_C+1)log x/(sqrt x+log x), a_C = 6(B_C+A_C+1),
C_tri(C) = 2(1+e^{X(C)}/3); printed numbering (3.1)–(3.4), (4.1)–(4.11), (5.1)–(5.10) = .tex labels in order.
Scripts + outputs: /tmp/oaimath/184/seats/T_work/{mech,negctl,split,rej_check,crossmass,leak,leakstep,scalars}.py

## Part A — line-by-line re-derivation

### Definitions in force
e_w(S,D) = sum_{u in S} sum_{v in D ∩ N(u)} w_u w_v (directed; §2). g_x(s) = s(x + log^+(1/s)), g_x(0)=0, nondecreasing
(derivative x+log(1/s)-1 >= 0 on (0,1) since x >= 1; x on (1,inf)). (3.1): for every x>=1, A,B: w(A),w(B)<=e^x ⇒
e(A,B) <= C g_x(w(A)). Note the asymmetry: the bound is in w(A), the FIRST (summed-over) set. I checked every use puts
the right set first (see 4.1(f)).

### Lemma 3.2 (preservation) — CORRECT
- "w(A_0) <= w~(A)": pi restricted to A surjects onto A_0, weights positive. OK.
- "The directed edges counted by e_H(A,B) map injectively to directed edges counted by e_G(A_0,B_0), with their weights
  unchanged": (a,b) with a in A, b in B∩N_H(a) ↦ (pi a, pi b), an edge of G (cond. 1) with pi a in A_0, pi b in B_0;
  injective by cond. 2. Then e_H <= e_G(A_0,B_0) <= C g_x(w(A_0)) <= C g_x(w~(A)) by monotonicity of g_x, and the
  hypothesis w(A_0),w(B_0) <= w~(A),w~(B) <= e^x is the right direction. Empty A: both sides 0. OK.
- M: injective on unordered edges (an unordered collision can be oriented into a directed collision). OK.
- Neighbourhood: pi injective on N_H(a) (else (a,b),(a,b') collide). OK.
- T: triangle ↦ 3 pairwise-adjacent hence distinct vertices; two triangles with one image share all three edges by
  edge-injectivity, hence coincide. OK. Composition preserves both conditions and weights. OK.
- Numerics (crossmass.py): EXACT best constant C*(G,w) = max over all (A,B) of e(A,B)/g_{x_min}(w(A)), x_min =
  max(1,log w(A),log w(B)) (sup is at minimal x since g_x increases in x), by full subset enumeration. 148 random
  (G, split-and-delete H) pairs, n_G in 4..7, n_H <= 13: max C*(H)/C*(G) − 1 = 2.2e-16 (equality cases only);
  M_H <= M_G, T_H <= T_G, nbhd bound all hold. NEGATIVE CONTROL: blowing one edge into K_{5,5} (not injective on
  directed edges) raises C* by up to 9.8x — the instrument can fail.

### Lemma 3.3 (normalisation and peeling) — CORRECT
- (3.2): sum over edges of w_u w_v c_uv counts each triangle once per edge (3T); sum_u w_u h_u counts it once per
  oriented edge (6T). h_u = 2 M_{G[N(u)]}. (3.3): c_uv <= s_u <= L. OK.
- (3.4): the loss at deleting edge i is exactly w_{u_i}w_{v_i}c_i (triangles through that edge in the current graph);
  telescoping; c_i < tau; deleted edges distinct so sum w w <= M_G. OK. Termination: finite.
- s_u >= c_uv >= tau via any remaining neighbour; h_u = sum w_v c_uv >= tau s_u. Cross-mass via inclusion map. OK.
- Numerics (mech.py, 3 seeds × 400 graphs): (3.2) to 7e-15 rel; telescoping |T0 − T1 − lost| to 9e-16; (3.4),
  s_u >= tau, h_u >= tau s_u, c >= tau all hold.

### Lemma 4.1 — CORRECT (every step)
(a) (4.2): s_u >= c_uv >= 1/x; h_u = sum_v w_v c_uv >= s_u/x. pi_u > 0 since c_uv > 0. OK.
(b) P_u row sums: sum_{z in N(u)∩N(v)} w_z / c_uv = 1. Ordered triangle law (4.4): mu(u,v)P_u(v,z) =
    (w_u w_v c_uv/Z)(w_z/c_uv) = w_u w_v w_z/Z. Conditional of v given u is pi_u; Z = 6T > 0 (an edge has c >= 1/x
    hence lies in a triangle). OK.
(c) Reversibility: pi_u(v)P_u(v,z) = w_v w_z 1{vz}/h_u symmetric. "Its powers, and hence Q_u and K_u^j, have the same
    properties": K_u^j = P_u Q_u^j is a POLYNOMIAL in P_u, and Pi p(P) is symmetric for every polynomial p when Pi P is
    symmetric. True (see E1 for the wording). Stationarity follows. OK.
(d) (4.5): P(v,y) = w_y/c_uv <= x w_y; K^j(v,y) = sum_z Q^j(v,z)P(z,y) <= x w_y (P,Q commute, Q^j stochastic).
    H_j >= −log x since a(y) <= x w_y in every term. OK.
(e) S_i(v), w(S_R) <= e^{20x^2}: double counting sum_y w_y w(N(y)∩S_i) = sum_{z in S_i} w_z s_z <= L w(S_i); Markov
    on the new vertices (threshold x^{-6}/L) gives at most L^2 x^6 w(S_i) of new weight, so w(S_{i+1}) <= (1+L^2x^6)
    w(S_i). log(1+e^{2x}x^6) <= log2+2x+6log x <= 4x (6 log x <= x for x >= 32: 6 ln 32 = 20.8); R <= x+1 <= 2x;
    total log-weight <= x + 8x^2 <= 20x^2. OK (scalars.py: holds on a grid x in [32,1e12]).
(f) (4.8) induction. i=0: P_u(v,·) supported on N(u)∩N(v) ⊆ S_0. Step: K^{i+1} = K^i Q. Mass from z ∉ S_i is at most
    the old leak i x^{-4}. For z ∈ S_i, y ∉ S_{i+1} ⊇ S_i: y ≠ z so Q(z,y) = P(z,y)/2 <= x w_y 1{zy}/2 (the paper
    drops the 1/2 — harmless); K^i(v,z) <= x w_z by (4.5) (z ∈ N(u), the only place the row lives — this answers the
    brief: the x w_z bound is applied only to z ∈ N(u), where (4.5) holds). Fresh mass at y <= x^2 w_y
    w(N(y)∩S_i) < x^2 w_y x^{-6}/L. Summing over y ∈ N(u): <= x^{-4} s_u/L <= x^{-4} because L = e^x >= s_u by (4.1).
    So (i+1)x^{-4}. OK. Note S_i(v) depends on v only, not on u — this is what lets one set serve every centre u ∈ N(v).
(g) B_v and the FIRST use of (3.1), parameter 20x^2 (>= 1): x^8 w(B_v) <= sum_{u in B_v} w_u w(N(u)∩S_R) <=
    e(N(v), S_R(v)); both sets' weights <= e^{20x^2} (w(N(v)) <= e^x; w(S_R) by (e)). Bound C s_v(20x^2 + log^+(1/s_v))
    <= C s_v(20x^2 + log x) <= 21 C x^2 s_v (s_v >= 1/x). So w(B_v) <= 21 C x^{-6} s_v. OK. Set order: A = N(v)
    (the bound is in w(N(v)) = s_v) — correct slot.
(h) Conditional law: by symmetry of mu the v-marginal is w_v h_v/Z and P(u|v) = w_u c_uv/h_v, so
    P(u in B_v | v) = e(B_v, N(v))/h_v exactly (leak.py: verified to 2e-16). SECOND use of (3.1), parameter x:
    w(B_v) <= w(N(v)) <= e^x, A = B_v first — correct slot. g_x(b) <= 2x max{b, e^{-x}} (b >= e^{-x}: log^+(1/b) <= x;
    b < e^{-x}: monotonicity). Then P <= C·2x(w(B_v)+e^{-x})·x/s_v; first piece 42 C^2 x^{-4}; second <= 2C x^3 e^{-x}
    (s_v >= 1/x) <= 2C x^{-4} using e^{-x} <= x^{-7} (x >= 7 ln x holds for x >= 32: 7 ln 32 = 24.3, and x − 7 ln x
    increasing for x > 7). Total E_C x^{-4}. OK.
(i) H_R <= A_C log x: (4.10) is −D(a‖w/m) + log m. For u ∉ B_v: D = N(u)∩S_R(v), w(D) <= x^8, delta = K^R(v, N(u)\S_R)
    <= R x^{-4} <= 2x^{-3} < 1, so D carries positive mass. Exact decomposition H_w(a) = (1−δ)H_w(a_D) + δH_w(a_{D^c})
    + h_bin(δ) <= log 2 + 8 log x + δ log s_u <= log2 + 8 log x + δx (signs fine even if a log is negative).
    On B_v: H <= log s_u <= x, probability <= E_C x^{-4}. So H_R <= log2 + 8 log x + R x^{-3} + E_C x^{-3}
    <= (10+E_C) log x (log2 + 2/x^2 <= 2 log x; E_C x^{-3} <= E_C log x). OK. Numerics: decomposition bound held on
    2,722 random splits (max violation 2.2e-16 = equality cases).
(j) (4.11): mixture identity sum_z q_z D(a_z‖b) = H_w(b) − sum_z q_z H_w(a_z) for b = sum q_z a_z is exact algebra
    (finite, b(y) >= q_z a_z(y) > 0 on the support). Q K^j = K^{j+1} (commuting). Averaging v ~ pi_u: the subtracted
    term becomes E_{z ~ pi_u Q_u} H_w(K^j(z,·)) = E_{v~pi_u} H_w(K^j(v,·) ) because pi_u Q_u = pi_u — this is exactly
    why stationarity makes it telescope. Average over u with weight w_u h_u/Z gives H_{j+1} − H_j. OK.
    Numerics: |H_{j+1} − H_j − E_{muQ} D| <= 5.5e-15 absolute over ~9,000 (graph, j) cases; monotonicity H_j <= H_{j+1}
    held throughout. Negative control: averaging over a UNIFORM start instead of pi_u breaks it by 6.9e-2.
(k) Telescoping: H_R − H_0 <= (A_C+1) log x, R increments, R >= x. OK. ONE index j for ALL u: yes — j is selected from
    the global average H_{j+1} − H_j, and every later use ((4.7), Lemma 5.2's H_j <= A_C log x, Lemma 5.3's corner
    bound) is a global mu-average, so no per-u choice is ever needed. H_j <= H_R <= A_C log x for j <= R by (4.6).
(l) TV <= sqrt(D): Jensen gives D >= −2 log sum sqrt(ab); −log t >= 1 − t gives >= sum(sqrt a − sqrt b)^2; C–S with
    sum(sqrt a + sqrt b)^2 <= 4 gives TV <= sqrt(D) (weaker than Pinsker, valid). Then Jensen E sqrt <= sqrt E. OK.
(m) mu-P to mu-Q passage: ||a_v − a_z|| <= ||a_v − b_v|| + ||b_v − a_z|| (triangle inequality), and
    E_mu||a_v − b_v|| + E_{muP}||a_z − b_v|| = 2 E_{muQ}||a_z − b_v|| EXACTLY because Q_u(v,·) = ½δ_v + ½P_u(v,·).
    Numerics: exact identity to 1.2e-15; final E_{muP}||a_v − a_z|| <= 2 sqrt(H_{j+1} − H_j) held for every j (not
    only the chosen one). Negative control: lazy weight 1/3 instead of 1/2 breaks the identity by 3.6e-2.
    And 2 sqrt((A_C+1) log x / R) <= 2 sqrt(A_C+1) sqrt(log x/x) = B_C sqrt(log x/x). OK.

### Lemma 5.1 (shared rejection) — CORRECT
P(Y_i = y) = sum_t (1−1/m)^{t−1} p_i(y)/m = p_i(y) (m = 1 fine with 0^0 = 1). By i.i.d. trials, the first trial
accepted by either row has "both accept" with probability sum min / sum max = (1−d)/(1+d) (sum min = 1−d,
sum max = 1+d with d = TV). So P(disagree) <= 2d/(1+d) <= 2d. Finite support: labels in J^I. OK.
Numerics (split.py, rej_check.py): marginals match (max z 3.2 over ~300 cells); I also derived the EXACT pair law
P(agree) = [(1−d) + sum (p−q)^+ q + sum (q−p)^+ p]/(1+d) (after a one-sided acceptance the other row restarts
fresh), confirmed by 4e5-sample simulation on 60 pairs (max |z| 2.28); the exact disagreement never exceeded
2d/(1+d) (equality e.g. for disjoint supports, where both equal 1).

### Lemma 5.2 — CORRECT
Law identity: mu(u,v)K(v,y) = [w_u h_u/Z] pi_u(v)K(v,y) = [w_u h_u/Z] pi_u(y)K(y,v) = mu(u,y)K(y,v), so
(u,v,y) =law (u,y,v). E ell = E log(w_y/K(v,y)) (after the swap) = E_mu H_w(K(v,·)) = H_j. ell >= −log x from (4.5)
applied to row y. Inadmissible ⟺ K(y,v) < w_v e^{-sqrt x} ⟺ ell > sqrt x. Markov on ell + log x >= 0:
P <= (H_j + log x)/(sqrt x + log x) <= (A_C+1) log x/(sqrt x + log x) for the chosen j < R. OK.
Numerics: law identity to 1.2e-15 rel, |E ell − H_j| <= 1.1e-14, ell >= −log x, Markov at 5 thresholds all hold.
Remark (not an objection): E ell = H_j uses reversibility; with a non-reversible start it fails (negative control
NC2: 0.75), so the reversed-transition admissibility rule is genuinely load-bearing and correctly justified.

### Construction of H' and Lemma 5.3 — CORRECT
- Groups are well defined when a label is inadmissible: A_{u,y} contains only ADMISSIBLE incidences with label y; an
  inadmissible incidence belongs to no group and its edge is not created; a vertex (u,y) exists iff A_{u,y} ≠ ∅, and
  every created edge's endpoints are of this form (both incidences admissible ⇒ v ∈ A_{u,Y_{u,v}}). OK.
- SIMPLE: (u,y) ≠ (v,y') as u ≠ v (no loops); a repeated pair would project to the same old edge, and each old edge
  creates at most one new edge (no multi-edges). OK.
- Projection injective on directed edges (old edge ↦ ≤ 1 new edge, orientation determined). OK.
- (5.2)/(5.4): N_{H'}(u,y) projects injectively into A_{u,y} (an edge also needs v's incidence admissible, so it is
  a subset), w(A_{u,y}) <= e^{sqrt x} sum_{v in A} K_u(y,v) <= e^{sqrt x} (row y of K_u sums to 1; y ∈ N(u)). Holds
  for EVERY outcome. OK.
- Survival is necessary AND sufficient: the three new edges are (u,Y_uv)(v,Y_vu), (u,Y_uz)(z,Y_zu), (v,Y_vz)(z,Y_zv);
  they exist iff all six incidences admissible, and close a triangle iff the copies coincide at each corner, i.e.
  Y_uv = Y_uz, Y_vu = Y_vz, Y_zu = Y_zv. At most one new triangle per old one. OK.
- Union bound: corner u: E P(Y_uv ≠ Y_uz) <= 2 E||K_u(v,·) − K_u(z,·)|| <= 2B_C sqrt(log x/x) by (4.7); corners v,z
  by the S_3-symmetry of the ordered-triangle law (weight w_u w_v w_z symmetric); each of the six directed incidences
  has marginal mu, and the inadmissibility event depends only on that incidence's label, whose marginal is K(v,·) —
  so delta_x each. 6B_C sqrt(log x/x) + 6 delta_x <= a_C log x/sqrt x using sqrt(log x) <= log x (x >= e) and
  sqrt x + log x >= sqrt x. "Some label vector has triangle mass >= its expectation": finite support. OK.
- Numerics (split.py, 3 seeds, ~270 graphs × 150 label draws, admissibility threshold s = a quantile of ell so that
  many labels are rejected): duplicate edges 0; non-injective directed images 0; image edges all in H; nbhd weight
  <= e^s, <= w(A_{u,y}), <= original nbhd (rounding only); triangle survival: actual \ predicted = predicted \ actual
  = ∅ in every draw (both directions of the characterisation); T' <= T, M' <= M. I computed the EXACT expected loss
  (corner pair laws are independent across corners; joint diagonal law from the exact pair formula): EXACT loss <=
  union bound in every graph (max excess 3.3e-16, equality cases), and Monte Carlo matches exact (max z 0.89).
  avg-over-triangles inadmissibility = 6 × avg-over-mu inadmissibility to 5e-15.

### Proposition 5.4 — CORRECT
- X(C) by (5.6): f(t) = log t/sqrt t has f' = (2 − log t)/(2t^{3/2}) < 0 for t > e^2 and f → 0, so X exists, depends
  only on a_C, i.e. only on C; for x > X >= 32 > e^2, a_C f(x) <= a_C f(X) <= 1/4, so 1 − a_C f(x) ∈ [3/4, 1].
  (For scale: C = 16·4^2 = 256 (r = 4) gives a_C ≈ 1.65e7 and minimal X ≈ 8.3e18; C_tri = 2(1+e^X/3) — astronomically
  large but finite and r-only. Irrelevant to correctness.)
- Peeling at tau = 1/x: T_H >= T_G − M_G/x; edge deletion keeps nbhd <= e^x and (3.1). Lemma 4.1/5.3 hypotheses on H:
  c >= 1/x, s <= e^x, (3.1), x >= 32, T_H > 0 — all met.
- H edgeless: G' empty; T_H = 0 gives T_G <= M_G/x, so RHS of (5.8) <= T_G − M_G/x <= 0 = T_{G'}. OK.
- Otherwise (1−ε)(T_G − M_G/x) >= (1−ε)T_G − M_G/x since 0 <= 1−ε <= 1. Composition H' → H → G is weight-preserving and
  directed-edge-injective, so Lemma 3.2 gives (3.1) with the SAME C and M_{G'} <= M_G. OK.

### Proof of Theorem 3.1 — CORRECT
- Termination: x_i = x_0^{2^{-i}} → 1 < X. Each G_i satisfies (3.1) with constant C (Prop 5.4 + induction), nbhd <=
  e^{x_i}. Constant C never degrades — this is the whole point of Lemma 3.2 and it is right.
- (5.9): f(t^2)/f(t) = 2/sqrt t <= 1/2 for t >= 16; parameters y^{2^m} with y = x_{k−1} > X; f decreasing on [X,inf);
  geometric sum <= 2f(y) <= 2f(X). Sum 1/x_i <= sum_m y^{-(m+1)} (2^m >= m+1) <= (1/X)/(1−1/X) <= 1. OK.
- The PRINTED iterate "T_k >= (prod(1−ε_i))T_0 − M_0 sum 1/x_i" (brief item 6): exact iteration of (5.8) gives
  T_k >= prod_{i<k}(1−ε_i) T_0 − sum_{i<k} [prod_{i<l<k}(1−ε_l)] M_i/x_i, and since the bracket is in [0,1] and
  M_i <= M_0 the printed form is a valid WEAKER consequence (induction step: multiply the possibly-negative lower bound
  by 1−ε_i >= 0, then use (1−ε_i)S_i <= S_i). Weierstrass prod(1−ε_i) >= 1 − sum ε_i >= 1/2 (needs ε_i ∈ [0,1]: yes).
  So T_k >= ½T_0 − M_0 survives. OK.
- 3T_k = sum_edges w w c <= e^X M_k (c_uv <= s_u <= e^{x_k} <= e^X), M_k <= M_0. Hence T_0 <= 2(1 + e^X/3) M_0 =
  C_tri M_0. k = 0 also covered (x_0 <= X). No dependence on n, x_0 or k. OK.

### (5.10) and circularity (brief item 8) — NO CIRCULARITY
§§3–5 use only positivity of weights and (3.1); no maximizer equation ((2.1) stationarity, (2.2) divergence) is
invoked anywhere after splitting — split weights are copies, not maximizers, and nothing needs them to be. (5.10)
applies Thm 3.1 once, to the maximizer w of F_G on the ORIGINAL K_r-free graph, using Lemma 2.3's bound (identical
in form to (3.1): bound in w(S) = first set, both weights <= e^x, every x >= 1) with C = 16r^2 >= 1 and positivity
from Lemma 2.1. §6 then applies (5.10) afresh to each G − A_v with ITS OWN maximizer. Constants: E_C, A_C, B_C,
a_C, X(C), C_tri(C) depend only on C; j depends on the graph but only through an existence statement.

### Scalar inequalities (scalars.py, mpmath 50 digits, x on a grid in [32, 1e12] dense near 32, C in {1,2,10,256,1e4})
6 log x <= x; log(1+e^{2x}x^6) <= 4x; R <= 2x; x + R log(1+e^{2x}x^6) <= 20x^2; 20x^2 + log x <= 21x^2;
e^{-x} <= x^{-7}; Rx^{-4} < 1; 42C^2x^{-4} + 2Cx^3e^{-x} <= E_C x^{-4}; H_R final chain; 2sqrt((A+1)log x/R) <=
B_C sqrt(log x/x) (equality at integer x, the 8 grid "failures" are 50-digit rounding at exact equality);
6B_C sqrt(log x/x) + 6delta_x <= a_C log x/sqrt x. All hold.

## Part B — EXPOSITION notes (none affects a constant or the theorem)
E1 (§4, Lemma 4.1 proof): "Its powers, and hence Q_u and K_u^j, have the same properties." A product of reversible
   kernels is not reversible in general; it is here because K_u^j = P_u Q_u^j is a polynomial in P_u. One clause
   ("being polynomials in P_u") would close the reader's gap.
E2 (§4, (4.8) step): "Q_u(z,y) <= x w_y 1{zy∈E(G)}" — true with a spare factor ½ (Q = P/2 off-diagonal). Harmless.
E3 (§5, proof of Thm 3.1): the displayed iterate is a weakening of the exact iterate (weights prod_{l>i}(1−ε_l) <= 1
   on the M_i/x_i terms dropped). Correct as an inequality; the text "Iterating (5.8) ... gives" could say "gives,
   after discarding factors in [0,1]". ½T_0 − M_0 survives.
E4 (§5, Prop 5.4 proof): "(5.6) ensures 0 <= 1 − a_C log x/sqrt x <= 1" — it in fact gives >= 3/4; fine as stated.
E5 (§5, Lemma 5.3): "There is a choice of these labels for which the projection preserves weights, maps directed edges
   injectively ... and satisfies (5.4)" — these three hold for EVERY label outcome; only (5.5) needs the choice. The
   proof says so; the statement merely bundles them.

## Part C — what I could NOT check
- Nothing in §§3–5 left unchecked. I did not replay the Lean (forbidden for this seat); I only noted that
  CliqueFree/ contains LocalWalk.lean (entropy_bounds, normalizer_eq = 6·triangleMass), FiniteEntropy.lean
  (entropy_mix_gap, tv_sq_le_hellinger, tv_triangle), Projection.lean (crossBound), Splitting/SplittingLoss.lean —
  i.e. the formal development has counterparts for each lemma here; whether they match the printed statements is
  seat L's question.
- §2 (Lemma 2.3 producing (3.1)) and §6 are other seats'; I used them only to confirm the interface (no circularity).
- Weak-evidence spot, stated plainly: the leakage claim (4.8) numerics (leak.py, leakstep.py) never produced a
  near-tight instance (one-step form held with min slack 0.05 over 2,988 cases; the full-chain version had zero
  leakage on every instance) — the bound is loose by construction (it spends K^i(v,z) <= x w_z), so numerics there are
  only a consistency check; the hand derivation in 4.1(f) is what carries it.
- Process note: crossmass.py's first run used multithreaded BLAS (~3.5 cores for 74 s) before I pinned
  OMP_NUM_THREADS=1; all later runs single-threaded.
