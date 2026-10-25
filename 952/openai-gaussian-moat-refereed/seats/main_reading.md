# Coordinator's own reading of OpenAI's "Bounded-Step Walks on Gaussian Primes" (family 28), 2026-10-22 00:0x–00:3xZ

Read from the LaTeX source (src/build/*.tex), all eight sections, before and while the seats ran. Printed numbering.
This is a reading by the coordinating model, not a human referee. Each item: what I checked, and the outcome.

## §1–2
- Theorem 1.2's set A(P) excludes BOTH conjugate factors of every selected split prime; periodic mod QZ² with Q = ∏p (true:
  pi | z depends only on z mod p since p = pi·conj(pi)). Changing associates does not change A(P) (true).
- Prop 2.1 proof: (i) locally finite + no infinite simple path ⇒ every component finite (König; correct). (ii) two points of a
  component differing by v ∈ QZ² ⇒ translation by v maps the component to itself (translation-invariance of the graph) ⇒
  impossible for a finite nonempty set and v ≠ 0 ⇒ injects into (Z/QZ)², size ≤ Q² (correct). (iii) Gaussian primes outside
  E (associates of the selected factors) lie in A(P) (a Gaussian prime divisible by pi is an associate of pi; correct);
  a component of G_D meeting E splits after deleting E into components of the A(P)-graph each adjacent to E, at most
  (K_D − 1)|E| of them (each needs an edge into E; correct, K_D counts 0) ⇒ the bound |E| + (K_D−1)|E|Q² (correct).
- The infinite-walk form needs only deleting an initial segment (finitely many exceptional primes; correct).

## §3
- (3.1): from Σ_{p≤x, p≡1(4)} log p ~ x/2 the batch weighted sum is (1/2+o(1))T and k_T ~ T/(2 log T) (correct).
- Lemma 3.1, 3.2 (continuity via a maximal coupling, applied to joint and marginal), 3.3 (Fano-type list bound,
  H(X|Y) ≤ h(ρ) + ρ log b + (1−ρ) log a; correct, b may be non-integer).

## §4
- Lemma 4.1: E in an R × 2W rectangle (projection argument correct); n+1 = O(RW) by disjoint disks (uses distinctness);
  the torus map (s,t) ↦ α(s) − γ(t) mod Λ is well defined on the parameter torus (endpoint differences a, −b) and is
  homotopic rel endpoints to (s,t) ↦ sa − tb, degree −1 ⇒ onto; every torus point within 2D of the image of a vertex
  difference ⇒ A ≤ 4πD²|E−E| (correct; collisions of projected differences only help).
- Lemma 4.2: collinearity of witnesses for sign vectors at Hamming distance ≤ dr/4: N(c*) ≥ P/(2T)^h, |det| ≤ 2R₁W₁ ≤ 2P^{1−d},
  log-ratio ≥ dr(log T − ¼ log 2T) − log 2 (correct). Fixed primitive line: witness = a·v with p_i | a for every pi_i ∤ v ⇒
  |witness| ≥ |v|P/P_σ(v); at most one factor over p_i divides primitive v; Σ over eligible ≤ 2 log|v| ⇒ E log P_σ ≤ log|v|
  (correct); Hoeffding with ranges log 2T (correct up to the absolute constant). Cube boundary inequality by induction
  (h₂(a) ≥ 1 − |1−2a|; correct). Distinct line classes at Hamming distance > dr/4 ⇒ radius ⌊dr/10⌋ balls disjoint; growth
  (1 + c d²) per step while relative size ≤ e^{−c₀d²r/2} ⇒ factor e^{c d³ r} (correct).
- Lemma 4.3: r ∈ [gq/2, 3gq] from log A ∈ [gU − O(1), 2gU + O(1)]; differences-of-differences in a rectangle of
  half-lengths ≤ (2R, 4W), the paper's (4R, 4W) is a safe over-estimate; P^{1−g} ≥ A^{1+3g} > 16A for g log A large
  (correct); injectivity on E−E except with prob O(e^{−cg³r}) by Lemma 4.2 with d = g; chain-rule display
  (enrichment-chain) correct (conditioning on all of h only lowers the subtracted entropy); subadditivity summed over the
  q−b remaining coordinates ≥ H(F_Q(X) | B_x, B_y, h) (correct direction); f_X(q) ≥ f_Z(q) − H(X − Z); concavity of f
  and of entropy under the ½–½ mixture (correct).

## §5
- Lemma 5.1 (correct). Theorem 5.2: Markov gives P(true residue on list) ≥ δ/(τ+δ) ≥ δ; Σ_x |(K−x)∩E| = u|E| ⇒ fewer than
  |E|/δ bad candidates; hit prob ≥ τ'(1−δ)u/p ≥ (τ+2δ)u/p; lower tail with v = δ/(τ+2δ) gives exp(−δ²np^{−β}/2);
  union bound; averaging η'/θ < δ/100; ā ≥ δ/2; list lemma with b = p^{1−β'/2}; h(ā) ≤ ā log(2e/δ); contradiction with
  Lemma 5.1 is strict because θ > η (all correct).

## §6
- Lemma 6.1: band arithmetic 0.05X_m − 1.3X_{m−1} = 0.05X_m − 0.013X_m = 0.037X_m (correct); offset N = ⌈T_+^{10}⌉ ⇒
  TV ≤ a/N ≤ T_+^{−9} (correct).
- §6.2 iteration d_{j+1} ≤ d_j/2 + C_D g ⇒ d_l ≤ 2^{−l} + 2C_D g; preservation costs O(gV)/(V/2) = O(g) (correct).
  Order of constants D, e₀ → l₀, g₀, c₀ → B → M stated and respected as far as I can see; (smaller-alphabet) uses only
  k_T log 2T ≤ CT and the geometric progression (Σ_{T'<T} ≤ CT/(B−1)).
- §6.3: J minimal with β_J log T ≤ M^{20}; r_i = 1/4 − 4β₀(1 − 2^{−i}) ∈ (0.23, 0.25] (β₀ = 1/200 ⇒ 4β₀ = 0.02; correct);
  checkpoints in the middle band since 0.23X_m < r_i log T ≤ 0.2625X_m; M³ iterations at g₁ = e^{−M³} consume O(M^6) of
  log-scale, the gap is 2β_i log T > 2M^{20} (correct).
- §6.4 Prop 6.2: τ_i = 3/8 − 2^{−i−3}, η_i = 100^{−(i+1)}2^{−i(i−1)/2−6i} (both recomputed from the recursions; correct);
  base case via Pinsker: each failing prime has TV ≥ (1−τ_J)p^{−β_J} ≥ c e^{−M^{20}}, average deficit ≤ e^{−90M^{20}}L*
  ⇒ failing fraction ≤ C L* e^{−88M^{20}} < η_J (correct). κ_i ≤ C_D·2T^{6β_i/5}·T^{r_i−2β_i}/T^{r_i}·e^{O(M^6)}
  = e^{−(4/5)β_i log T + O(M^6)} ≤ e^{−M³} (correct). Transfer hypotheses: δ₀ = 1/64, τ ≤ 3/8, β' = β/2 ≤ β, η' = ηδ/100
  (equality), n_i p^{−β_i} ≥ ½ e^{M^{20}/5} dominating log p ≤ 1.05·100^M + log 2 and log(100/δ) = O(M); δ^{−1} < p^{β'/2}
  and log(2e/δ) ≤ (β'/4) log T from β_{i+1} log T > M^{20}/2 (all correct). Conclusion at A₀: mass ≥ 1/(4p) outside fewer
  than p^{199/200} residues for ≥ 99% of signed primes.

## §7
- E_C H(X | O) ≥ (1 − 2e₀)qL* from (global-entropy) and (smaller-alphabet) (correct). H(s) = O_D(T^{1/4}) from
  (native-data) at r₀ = 1/4 (correct: scales are logarithms of time lengths, so the displacement alphabet is e^{O(T^{1/4})}).
- True residue passes every package (each package continues the actual zero-avoiding walk from a time with that residue;
  correct). Unfavourable count ≤ 2η₀q via the tower property with C independent of the walk (correct).
- Hit probability ≥ τ₀/(2p) at each offset l < L by smoothing (l ≤ T_+; T_+^{−9} ≤ τ₀/(2p)), mixture ≥ τ₀/(8p) (correct).
  Disjointness of hits within one package: two hits ⇒ two walk points with equal residues mod pi at distance ≤ DL < √p,
  nonzero by self-avoidance, contradiction (correct; needs DL < √T, i.e. D·T^{2/5} < T^{1/2}, true for large T).
- E|list| ≤ 4p^{1−β₀} + p exp(−cLm_T/p) ≤ 5p^{1−β₀}; entropy bound ≤ (1 − β₀/2)qL*; I(X;P|O) ≥ (β₀/2 − 2e₀)qL* =
  0.46β₀qL* ≥ (β₀/3)qL* (correct with e₀ = β₀/50). Transport: I(X;P|O) ≤ m_T·I(X; s,W | O) by conditional independence;
  I(X; s,W | O) ≤ I(X'; W | O') + 2H(s) (bijection given s + the displayed identity; correct). Final:
  ≥ (β₀c₀/(6K₀))·L/log T − O(T^{1/4}) with L ≥ ½T^{2/5} (correct).

## §8
- a_j − b_j = I(X'_{T_j}; W_{L_j}(t*) | O'_{T_j})/L_j (O' = Q_{j−1}, (O', X') = Q_j; correct). Block chain rule with
  Q_j(t*+a) a function of Q_j(t*) and the earlier increments (correct). Continuity with TV ≤ T_+^{−9}, alphabet log-size
  O(T_+) ⇒ ε_M = O(T_+^{−7}); n_B = O(log T_+) batches ⇒ total error o(1) (correct). a₁ ≤ log K_D, b_{n_B} ≥ 0.
- Final count: each window [X_m, 1.05X_m] holds ≥ cX_m/log B values j·log B, each contributing ≥ 1/(1.05X_m) ⇒ ≥ c/(1.05 log B)
  per window, ~M/2 windows ⇒ divergence vs the fixed log K_D (correct). P_D = P_M for one M depending only on D; the auxiliary
  choices C only average inequalities (correct).

Nothing found that I would call a gap. Things I did not verify to the last constant: the absolute constants in Lemma 4.2
(Hoeffding / enlargement), the O(·) bookkeeping that every error in Lemma 4.3 is o(g) uniformly; these are exactly what
the Lean formalisation checks, and the replay is green.
