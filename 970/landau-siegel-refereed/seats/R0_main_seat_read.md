# R0 — the main seat's own read (written 2026-10-26 ~09:25Z, BEFORE any panel report came back)

Read: all 773 lines of paper.tex, every lemma, line by line. Verdict on my own read: HOLDS AS READ. No gap found.

## The argument in one paragraph
A real zero with δ = (1−β)log q small forces almost all log-mass of primes up to X = q^{O(1)} onto χ(p) = −1 (Lemma 2, the standard
Hadamard/log-derivative inequality). In K = Q(√d, √2), those primes have Frobenius σ or στ, so θ^p ≡ σθ or στθ (mod pR). Build an
N^4 × N^4 determinant Δ of monomials θ^α1 σθ^α2 στθ^α3 evaluated at θ_n (n ∈ {0..N−1}^4): 4-dimensional integer points seen through
only THREE conjugates, so the natural degree is U = N^{4/3}. Rows are chosen greedily in the weight order α1 + Hα2 + Hα3 so nearly all
degree sits on θ. Frobenius replacement θ^p → g_p(θ) lowers weight by p − H > 0, so (unit lower-triangular change, over K) Δ ∈ p^{E_p}R
with E_p = Σ⌊α1/p⌋. Divisibility gives log|NΔ| ≳ 4·S1·log U; Hadamard gives log|NΔ| ≲ 4·S1·(log N + ½ log q) = 4·S1·(¾ log U + ½ log q).
With N = q^γ, γ large, the 4/3 gain wins: contradiction as δ → 0.

## Step checks (what I verified, not what I assumed)
- Lemma 2 (p.2): (2.3) is Davenport ch.12/14 (Re 1/(s−ρ) ≥ 0 for s>1; real s, real χ ⇒ −L'/L real). s = 1+1/log X gives p^{−s} ≥ p^{−1}/e
  for p ≤ X; 1/(s−1) − 1/(s−β) ≤ (1−β)(log X)². (2.2) via Mertens + Σ_{p|q} log p/p ≤ log q. Correct, uniform in q.
- Lemma 3 (pp.3–5), the zero estimate — the place I expected a hole. Checked every step: R exists by dimension count (4P ⊂ [0,4(N−1)]^4);
  R∘A ≠ 0 (A surjective) cannot vanish on Z^4; minimiser m exists (finitely many lattice points near compact K); h = m − y ≠ 0;
  nearest-point inequality ⇒ y/4 in the h-maximal face G; G proper when P is 4-dim (h ≠ 0); Carathéodory in dim ≤ 3 ⇒ ≤ 4 vertices,
  one weight ≥ 1/4 ⇒ y − u ∈ 3P (weights (4λ_u − 1), 4λ_i, sum 3); for n ∉ G, h·(u − n) > 0 strictly, so (3.5) gives a strictly
  closer lattice point m' with R(Am') = 0; rational hyperplane ⊃ G with r·c ≠ 0 by Q-independence ⇒ A|_H bijective; Lagrange Q has
  total degree ≤ 3(N−1) and kills (S∩G)∖{u} because two points of H agreeing off i0 coincide; B = Q·R(·+A(m−u)) ∈ P_t; contradiction
  v_u R(Am) ≠ 0. HOLDS.
- Corollary 4: T_j ≥ 32N iff N ≥ H; Π(T_j − 3N) ≥ T1T2T3/8 = 4096N^4 > (4N−3)^4. HOLDS.
- §4: ker A = C(ab, b, −a, −1) — multiplied out all three rows, zero. Coordinates Q-independent since [K:Q]=4 (d squarefree, ≠ 1, 2).
  Greedy over N^3 in weight order is a well-order of type ω (finite weight classes); all retained weights ≤ T1 + H(T2+T3) = 96H^{2/3}U
  because the box rows are all processed before any heavier row and already span. HOLDS.
- Lemma 6: α2, α3 ≤ 96H^{−1/3}U; ≤ Q0 retained indices per α1 value ⇒ S1 ≥ M²/(2Q0) − M/2 ≥ M²/(4Q0). HOLDS (H must be ~10^8 for
  (C0/c0)/H ≤ 1/12 — fine, H is fixed).
- Lemma 7 (p.7) — my first suspicion was p-integrality of the change of basis; the paper anticipates it and is right: R̃_α is computed
  DIRECTLY as θ^r(θ^p − g_pθ)^k σθ^{α2} στθ^{α3}, whose entries lie in p^k R by (5.2); separately R̃_α = R_α + (K-combination of rows of
  strictly smaller weight), each in the K-span of retained rows strictly before α ⇒ R̃ = L·R with L unit lower-triangular over K ⇒
  det R̃ = Δ; factor p^k out of each row of R̃ (entries in p^k R) ⇒ Δ ∈ p^{E_p}R. No integrality of L needed. (5.2): a^p = a·d^{(p−1)/2}
  ≡ (d/p)a = −a (p ∤ d since p ∤ q), b^p ≡ (2/p)b; Frobenius of x+ya+zb+wab is σθ if (2/p)=1, στθ if (2/p)=−1. Checked both. HOLDS.
- (5.1): |ν(θ_n)| ≤ (N−1)(1+√|d|)(1+√2) ≤ 8N√q, both signs of d. Hadamard: row norm ≤ √M·max entry. HOLDS.
- (5.6)–(5.7): ⌊x⌋ ≥ x − 1 per row; Chebyshev; Lemma 2 at X = U. HOLDS.
- §6 order of choices: H first (absolute, via C0/c0), then γ (depends on absolute C and the fixed bound S2/S1 ≤ 1/12), then q → ∞ along
  the sequence. ℓ/log U → 3/(4γ); δ log U/ℓ → 0; MU/(S1 log U) ≪ H^{−2/3}/log U → 0. 1 ≤ 13/16 + 1/16 = 7/8. No hidden dependence.
- §6 reduction: finitely many χ of bounded conductor, L(1,χ) ≠ 0, continuity ⇒ q → ∞; Q(√d) = Q(√2) only for d = 2 (one field).

## Sanity test (does the method prove something false?)
The divisibility step works for ANY prime p whose Frobenius in Gal(K/Q) lies in {1, σ, στ} — the three conjugates used as variables —
because θ^p ≡ θ, σθ or στθ, each of weight ≤ H < p. It does NOT work for Frobenius τ (τθ is not a monomial in the three variables).
So the unconditional content of the argument is: the log-density of primes ≤ U = q^{4γ/3} with Frobenius in {1, σ, στ} is at most
(3/4)(1 + S2/S1) + O(1/γ) — and Chebotarev says that density is exactly 3/4 for fixed q, U → ∞. The bound is SHARP, not violated: the
method proves a true statement with no slack to spare (as H, γ → ∞). A Siegel zero pushes the {σ, στ} classes alone to density ≈ 1 > 3/4.
This is the strongest evidence I have that the argument is not "too good": an error that inflated the divisibility side would
contradict Chebotarev; this one sits exactly on it.

## What I did NOT check
The Lean (seat D). Literature/world (seat W). Exact small-case computation of Δ (seat C). The QRH 7/8 paper (199 pp.) is out of scope.

## Addendum (~09:35Z, still before any report): the sanity test, generalised
The heavy variable can be any conjugate gθ in a 3-subset S ∋ g of Gal(K/Q); Frobenius g_p is usable iff g_p ∈ S·g^{−1}, a set that always
contains 1. So the method bounds, for each non-identity class c ∈ {σ, τ, στ}, the log-density of the complement of {c} by 3/4 + ε, i.e.
gives density(c) ≥ 1/4 − ε on [1, q^γ] — every non-identity Frobenius class gets at least its Chebotarev share, and the identity class
gets nothing (as it must: the method never sees it from below). For fixed q this is exactly Chebotarev (each class 1/4): consistent, no
slack. Equivalent in strength to a Brun–Titchmarsh bound with constant 1 + ε instead of 2 for these classes — which is precisely the kind
of statement known to be equivalent to excluding Siegel zeros (Motohashi). So the method is as strong as it has to be, and no stronger.
