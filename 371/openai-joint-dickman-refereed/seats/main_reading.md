# Coordinator's own reading (06:00Z erdos seat, 2026-10-22) — §1 and §11 of OpenAI family 012

Read in full: §1 (introduction.tex) and §11 (distribution.tex). Seats A (§1.2, §§2–4), R (§§5–11), L (Lean), W (world) cover the rest.

## §11 — checked
- §11.1 Fourier inversion: count vectors b_x(m) ∈ {0..J}^{J−1} (each counted prime > x^{1/J}, m ≤ x ⇒ ≤ J factors); reduction mod J+1
  injective; the indicator identity is the standard finite Fourier inversion on (Z/(J+1))^{J−1}. Rational c, d: choose J with both
  on the grid; P⁺(m) ≤ x^c ⇔ all counts in bins with lower endpoint ≥ x^c vanish. Sound.
- Lemma 11.1 (Dickman marginal): inclusion–exclusion over falling factorials of N_{c,x}(m) ≤ J (finite sum), factorial-moment limits
  from §2; I_h(y) − I_h(z) = h∫_z^y I_{h−1}(t−1) dt/t ⇒ uH'(u) = −H(u−1), H = 1 on [0,1] ⇒ H = ρ (uniqueness by successive
  integration). Irrational c by monotone sandwich + continuity of ρ. Sound.
- (11.6)–(11.7) fixed thresholds through real X: x = ⌊X⌋ + 1 and rational c_± sandwich. Sound (x/X → 1; X^c between x^{c−}, x^{c+}
  for large X).
- Proof of Theorem 1.1 (moving thresholds n^a): on εX ≤ n ≤ X, X^{c−} ≤ n^a ≤ X^{c+} for large X; initial segment costs ε. Sound.
- Proof of Cor 1.2: clamp V_n to [0,1] (overshoot ≤ 1/(N log N)); joint CDFs at interior (a,b) converge to D(a)D(b); interior
  rectangles determine the law ⇒ weak convergence to D⊗D; diagonal has product mass 0 (D continuous) ⇒ portmanteau ⇒ 1/2 each.
  Sound.

## Consequences the paper does not state (ours, label (b) modulo Thm 1.1)
- Erdős [Er79e] α-question: {P(n+1) > P(n)·n^α} = {V_n > U_n + α}; the line v = u + α has D⊗D-mass ∫ μ({u+α}) dμ(u) = 0 since μ
  is atomless; same portmanteau step ⇒ density exists = ∫∫_{y>x+α} f(x)f(y), f(t) = ρ(1/t − 1)/t (Teräväinen's log-density formula).
  Seat R and seat W reached the same conclusion independently.
- #928 as posed (strict, (n+1)^β): sandwich between the paper's events at (α−δ, β−δ) and (α, β+δ) + continuity ⇒ ρ(1/α)ρ(1/β).
  Proved in Lean in bridge/Bridge371.lean (EPAD371.erdos_928). jbaelaw/Erdos928 (9–10 Oct) formalized the implication first
  (joint law as hypothesis, count-bound route).

## Numerics (compute/)
- lpf_count.c (segmented sieve, division) to 1e10: inc 4,999,983,166 / dec 5,000,016,833 (sum = 1e10 − 1).
- lpf_numpy.py (ascending-prime overwrite, no division) to 1e8: identical at every checkpoint; 16 joint counts identical at 1e7.
- July report runs/erdos371_wave8y.md (third program): A(X) = ours + 1 (it counts n = 1) at every 10^k ≤ 1e8.
- OEIS A070089 b-file (1,000 terms, n ≤ 1,981): identical list.
- rho_check2.py: OpenAI's `rho` definition (grid Picard + mpmath) vs Heun ODE vs literature: agree to ~1e-9.
- alpha_count.c to 1e9 + alpha_predict (product-law integral): counts decrease toward predictions slowly (table in entry).
- indep_ratio_1e10.txt: joint/(marginal·marginal) rises toward 1 at every tested (a,b).
