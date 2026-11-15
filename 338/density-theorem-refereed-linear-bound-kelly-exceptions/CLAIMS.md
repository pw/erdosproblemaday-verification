# Erdős #338 — claims under review (2026-11-15, erdos cron seat)

Definitions. A ⊆ ℕ = {1, 2, 3, …} (positive integers; 0 ∉ A — the referee's SHOULD 1). *Order* h: every sufficiently large integer is a sum of at most h elements of A, repetition
allowed. *Restricted order* t: every sufficiently large integer is a sum of at most t DISTINCT elements of A.
d(·) = lower asymptotic density. A is *robust* if A \ F is a basis for every finite F.

## V1 — Veljjanoski's Theorem 1 (his; `dl/repo/README.md`, commit 9429d6f, 1 Oct 2026)
If d(A) = δ > 0 and for every modulus g the residue classes mod g containing infinitely many elements of A generate
ℤ/gℤ, then every sufficiently large integer is a sum of at most 3s − 2 distinct elements of A, s = ⌈8/δ²⌉.

## A — our sharpening (ours, to be refereed): the bound is LINEAR in 1/δ
**Theorem A.** Same hypotheses. Every sufficiently large integer is a sum of at most 3⌈8/δ⌉ − 2 distinct elements of A.

Proof. Identical to V1 except Step 1, which becomes:

*Step 1′: d(M_R) ≥ δ/4 for every R ≥ 1*, where r(n) = #{(a,b) : a < b, a,b ∈ A, a + b = n}, M_R = {n : r(n) ≥ R}.
Fix ε ∈ (0, δ), let N be large, x = N/2, A(x) = |A ∩ [1,x]| ≥ (δ − ε)x.
(i) Every pair a < b in A ∩ [1,x] has a + b ≤ N, and distinct pairs are counted in Σ_{n≤N} r(n) once each, so
    Σ_{n ≤ N} r(n) ≥ C(A(x), 2).
(ii) If n ≤ N and a < b, a + b = n, then a < n/2 ≤ x, and a determines b. So r(n) ≤ |A ∩ [1,x)| ≤ A(x).
     [V1 used r(n) ≤ n/2 ≤ x here; that is the only change.]
(iii) For n ∉ M_R, r(n) ≤ R − 1. Hence
      C(A(x),2) ≤ Σ_{n ≤ N} r(n) ≤ A(x)·|M_R ∩ [1,N]| + (R − 1)·N,
      |M_R ∩ [1,N]| ≥ (A(x) − 1)/2 − (R − 1)N/A(x) ≥ (δ − ε)N/4 − 1/2 − 2(R − 1)/(δ − ε).
So d(M_R) ≥ (δ − ε)/4 for every ε, i.e. d(M_R) ≥ δ/4.

(Kneser's theorem does not need 0 ∈ M_R; if a source requires it, apply it to M_R ∪ {0}, which gives "at most s"
popular summands and only helps Step 4 — referee's SHOULD 7.)
Steps 2–4 as in V1 with s = ⌈8/δ⌉: s·d(M_R) ≥ 2 > 1 ≥ d(sM_R); Kneser ⇒ g ≤ s − 1 and all large n ≡ y₀ (mod g) lie
in sM_R; residue fixed by a set E_t of ≤ g − 1 ≤ s − 2 distinct elements; R = 3s; greedy choice of disjoint pairs.
Total ≤ (g − 1) + 2s ≤ 3s − 2. ∎

**Corollary A.** Let T(δ) be the largest restricted order of a set satisfying the hypotheses with lower density ≥ δ.
For δ = 2/m (m ≥ 2): m − 1 ≤ T(2/m) ≤ 12m − 2 (i.e. 2/δ − 1 ≤ T(δ) ≤ 24/δ − 2 at these δ only; in general
⌊2/δ⌋ − 1 ≤ T(δ) ≤ 3⌈8/δ⌉ − 2 — referee's SHOULD 2). (Lower bound: Veljjanoski's example
A = {n ≡ 0 or 1 mod m}, restricted order exactly m − 1.) So the right dependence on δ is linear in 1/δ — the
question his note leaves open ("Whether the right dependence on δ is linear in 1/δ is left open").

Remark (not for the headline unless checked): for any integer s with sδ/4 > 1 the same proof gives
g ≤ (s − 1)/(sδ/4 − 1) and at most 2s + g − 1 summands (need R > g − 1 + 2(s − 1)).

## A″ — STRONGER FORM (added 09:3xZ; this is now the headline claim; Theorem A above becomes a corollary)
**Lemma 1″.** If A ⊆ ℕ has lower density δ > 0 then d(M_R) ≥ δ for every R ≥ 1 (M_R = integers with at least R
representations a + b, a < b, a, b ∈ A).

Proof. Fix R and an integer K ≥ 1. Let a_1 < … < a_K be the K smallest elements of A. For N > a_K put
B_N = A ∩ (a_K, N], so |B_N| = A(N) − K. For 1 ≤ i ≤ K and b ∈ B_N the pair (a_i, b) has a_i < b, both in A, and
a_i + b ≤ N + a_K. Let c(n) = #{(i, b) : 1 ≤ i ≤ K, b ∈ B_N, a_i + b = n}.
 (i) c(n) ≤ K (i determines b = n − a_i).
 (ii) c(n) ≤ r(n) (different (i, b) are different pairs a < b with sum n).
 (iii) Σ_n c(n) = K(A(N) − K), and every n with c(n) > 0 satisfies n ≤ N + a_K.
Split the sum: for n ∈ M_R use (i); for n ∉ M_R use (ii), r(n) ≤ R − 1. With N′ = N + a_K:
   K(A(N) − K) ≤ K·|M_R ∩ [1, N′]| + (R − 1)·N′,
   |M_R ∩ [1, N′]| ≥ A(N) − K − (R − 1)N′/K.
Divide by N′ and let N → ∞ with K fixed (N′/N → 1): d(M_R) ≥ δ − (R − 1)/K. K is arbitrary, so d(M_R) ≥ δ. ∎
(Sharp: A = multiples of m has M_R = large multiples of m, density exactly δ.)

**Theorem A″.** Under the hypotheses of V1 (lower density δ > 0; for every g the infinitely-populated classes mod g
generate ℤ/gℤ), every sufficiently large integer is a sum of at most 3⌈2/δ⌉ − 2 distinct elements of A.
Proof: V1's Steps 2–4 with s = ⌈2/δ⌉ and Lemma 1″: s·d(M_R) ≥ 2 > 1 ≥ d(sM_R) ⇒ Kneser ⇒ g ≤ s − 1; E_t of size
≤ g − 1 ≤ s − 2; R = 3s; total ≤ (g − 1) + 2s ≤ 3s − 2. ∎

**Corollary A″.** For δ = 2/m (m ≥ 2): m − 1 ≤ T(2/m) ≤ 3m − 2. For every δ ∈ (0, 1]:
⌊2/δ⌋ − 1 ≤ T(δ) ≤ 3⌈2/δ⌉ − 2 < 6/δ + 1 (lower bound: the example with m = ⌊2/δ⌋). So the answer to "is the dependence linear in 1/δ" is yes, within a factor 3.
Numbers for the page: δ = 1/5: V1 gives 3·⌈200⌉ − 2 = 598; A″ gives 3·10 − 2 = 28.

## C — the linear bound from Erdős–Nathanson–Sárközy 1988 (added 09:4xZ after the world seat found the paper)
Source: P. Erdős, M. B. Nathanson, A. Sárközy, Sumsets containing infinite arithmetic progressions, J. Number Theory 28
(1988) 159–166 (scan: world/src/erdos_1988_33.pdf, text .txt). NOT cited in Veljjanoski's note, on the forum, or in our
July report. Notation there: d_L = lower density, ⟨w⟩ = ceiling, hA = h-fold sumset, h^A = sums of h DISTINCT elements,
A^(g) = {a′ > 0 : a′ ≡ a (mod g) for some a ∈ A}, X ∼ Y = equal from some point on.
 - Kneser (their form, p. 161): either d_L(hA) ≥ h·d_L(A), or there is a minimal g ≥ 1 with hA ∼ hA^(g) and
   d_L(hA) ≥ h·d_L(A) − (h − 1)/g.
 - Lemma 1 (Szemerédi): A′ = {a ∈ A : a + id ∈ A for some d > 0 and all |i| < t} has d(A \ A′) = 0.
 - Lemma 2: with t = h, hA′ ⊆ h^A.
 - Theorem 1 (stated): d_L(A) = w ∈ (0, 1/2], k = ⌈1/w⌉ ⇒ (k+1)^A contains an infinite AP of difference g ≤ k² − k, and
   (k² − k)^A one of difference g ≤ k + 1.
 - Its PROOF gives, for every integer s ≥ 1: there is g with g = 1 or 1 < g ≤ k + (k² − 2k)/s such that
   (k+s)A′ ∼ (k+s)A′^(g) (A′ taken with t = k + s). [From (k+s)w − (k+s−1)/g ≤ d_L((k+s)A′) ≤ 1 − 1/g and w ≥ 1/k.]
   Hence every sufficiently large integer in the residue class of any y₀ ∈ (k+s)A′ is a sum of k + s DISTINCT elements of A.

**Theorem C (derived here; rigorous modulo Kneser's and Szemerédi's theorems as used by ENS).** Let A ⊆ ℕ have lower
density δ ∈ (0, 1/2] and suppose that for every g the residue classes mod g containing infinitely many elements of A
generate ℤ/gℤ. Then every sufficiently large integer is a sum of at most 4⌈1/δ⌉ − 4 distinct elements of A.

Proof. k = ⌈1/δ⌉ ≥ 2, s = k − 1, G = 2k − 2. For every g ≤ G and every class u mod g fix a set E_{g,u} ⊆ A of at most
g − 1 distinct elements with ΣE_{g,u} ≡ u (mod g) (exists: V1's Step 3). E = ⋃ E_{g,u} is finite. A₀ = A \ E has
lower density δ. Apply the ENS proof to A₀ with this s: we get g = 1 or 1 < g ≤ k + k(k − 2)/(k − 1) < 2k − 1, so
g ≤ 2k − 2 = G, and y₀ such that every large m ≡ y₀ (mod g) is a sum of k + s = 2k − 1 distinct elements of A₀.
For large n put u ≡ n − y₀ (mod g): n − ΣE_{g,u} is large and ≡ y₀, so it is a sum of 2k − 1 distinct elements of
A₀ = A \ E, and E_{g,u} ⊆ E is disjoint from them. Total ≤ (2k − 1) + (g − 1) ≤ 4k − 4. (If g = 1: 2k − 1 ≤ 4k − 4.) ∎

Numbers: δ = 1/2: 4; 1/5: 16; 1/10: 36; 1/50: 196. Lower bound (Veljjanoski's example): ⌊2/δ⌋ − 1 = 3, 9, 19, 99.
So for δ ≤ 1/2: ⌊2/δ⌋ − 1 ≤ T(δ) ≤ 4⌈1/δ⌉ − 4; the ratio of the two is at most 8/3 (just below δ = 1/2: 3 vs 8),
is (4k−4)/(2k−1) < 2 at δ = 1/k, and tends to 2 as δ → 0 (referee's MUST: NOT "a factor 2" uniformly). s = k − 1 is the
optimal choice in this method (min over s equals 4k − 4 for k = 2..60). The hypothesis δ ≤ 1/2 is not needed (any δ < 1),
and the residue hypothesis is used only for g ≤ 2k − 2. ENS's stated Theorem 1 has two harmless slips at k = 2 (Lemma 2
needs t ≥ h; s = 0 in part (ii)); Theorem C uses their proof with t = k + s and s = k − 1 ≥ 1. A″ (3⌈2/δ⌉ − 2 = 10, 28, 58, 298) is weaker but avoids Szemerédi's
theorem and changes only one step of the note's own proof.

WHAT IS OURS NOW: (1) the observation that ENS 1988 + the note's Step 3 answer the note's open question, with the
derivation of Theorem C; (2) Lemma 1″ / Theorem A″ as an elementary route; (3) Theorem B. The linear dependence itself
should be credited to the ENS method, not to us.

## V2 — Veljjanoski's Theorem 2 (his): block model, order 3
For every finite C ⊂ (1,∞), l*(C,3) ≤ 4 (definitions in the README). `block338.py` is his exact-rational code.

## K — the Kelly counterexample (his Lean proof in formal-conjectures #7788, 8 Nov 2026) and its exception set (ours)
X = {a ≥ 0 : every base-3 digit of a is 0 or 1}. A = {2a + 1 : a ∈ X} ∪ {4a : a ∈ X, a ≥ 1}. (The Lean set
`ternaryBasis` also contains 0 = 4·0; a summand 0 never helps, so this is immaterial — referee's SHOULD 4.)
His claims (Lean, `FormalConjectures/ErdosProblems/338.lean`): A has order 2 (in fact EVERY n ≥ 1 is a sum of at most
two elements), and no n = 2·3^j is a sum of at most three distinct elements. Hence Kelly's conjecture (order 2 ⇒
restricted order ≤ 3) fails. [Hennecart 2005 disproved it first; the description of pull request 7788 (not the Lean file) says "We could not
access [He05], so it may differ from Hennecart's construction" — referee's SHOULD 5.]

**Theorem B (ours).** (1) A positive integer n is NOT a sum of at most three distinct elements of A if and only if
n = 2·3^j for some j ≥ 0. (2) Every positive integer except 2, 6, 18 is a sum of at most four distinct elements of A.
So the restricted order of A is exactly 4 and the exceptions to "3" up to N number ⌊log₃(N/2)⌋ + 1.

Proof of (1). Odd n: (n − 1)/2 = a + 2c with a, c ∈ X (digit by digit: digit 0 → (0,0), 1 → (1,0), 2 → (0,1), no
carries), so n = (2a + 1) + 4c, one or two distinct elements (odd ≠ multiple of 4; if c = 0 it is one element).
Even n: a representation by ≤ 3 distinct elements uses 0 or 2 odd elements.
Key Lemma: for an integer k ≥ 0, the equation a + b + 2c = k has a solution a, b, c ∈ X with a ≠ b iff k is not
of the form 3^j − 1 (j ≥ 0).
 (⇐, "only if" direction of the lemma) k = 3^j − 1: Lean lemma `Ternary01.eq_of_add` (induction on digits; the last digit of a + b + 2c is
 2 only for (a₀,b₀,c₀) ∈ {(1,1,0), (0,0,1)} with no carry... the general step handles carries by the identity
 (a + b + 2c + 1 = 3^j, reduce mod 3, divide by 3)). So a = b.
 (⇒) Let i be the least index with digit d_i(k) ≠ 2 (exists unless k = 3^i − 1 with all i digits 2 — and if k has
 digits 2 in positions 0..i−1 and nothing else it is 3^i − 1). Put (a_l, b_l, c_l) = (0,0,1) for l < i (digit 2, no
 carry). If d_i = 1: (a_i,b_i,c_i) = (1,0,0), no carry, and complete with a′ + 2c′ = ⌊k/3^{i+1}⌋, b′ = 0.
 If d_i = 0 and k′ = ⌊k/3^{i+1}⌋ ≥ 1: (a_i,b_i,c_i) = (1,0,1) (sum 3 = digit 0, carry 1), complete with
 a′ + 2c′ = k′ − 1, b′ = 0. If d_i = 0 and k′ = 0 then k = 3^i − 1. In both constructed cases a_i ≠ b_i.
 n ≡ 2 (mod 4): two odd elements are forced (a sum of ≤ 3 multiples of 4 is ≡ 0 mod 4; one odd element gives odd
 sum), so n = (2a+1) + (2b+1) [+ 4c], a ≠ b, i.e. a + b + 2c = (n − 2)/2 =: k (c = 0 means no third element).
 By the lemma this is solvable iff k ≠ 3^j − 1 iff n ≠ 2·3^j.
 n ≡ 0 (mod 4): k = (n − 2)/2 is odd, 3^j − 1 is even, so the lemma gives a representation
 n = (2a+1) + (2b+1) + 4c with a ≠ b (if c = 0, two elements).
Proof of (2): n = 2·3^j, j ≥ 3: take the two multiples of 4 to be 12 = 4·3 and 16 = 4·4 (3 = 10₃, 4 = 11₃ ∈ X);
need a + b = 3^j − 1 − 14 with a ≠ b ∈ X; 3^j − 15 = 2…2110₃ for j ≥ 3 (26 − 14 = 12 = 110₃; in general
3^j − 1 − 14: subtract 112₃ from 2…222₃ digitwise = 2…2110₃, no borrows), which has digits in {0,1,2} with a digit 1,
so a + b = it has a solution with a ≠ b (digit 2 → (1,1), 1 → (1,0), 0 → (0,0)). 2, 6, 18: finite check.

Computation (instrument 1, `kelly/ternary_bitset.py`, N = 300,000): order-2 check 0 misses; exceptions for ≤ 3
distinct = {2, 6, 18, 54, …, 118098} = {2·3^j ≤ N}; exceptions for ≤ 4 distinct = {2, 6, 18}.

## What is NOT claimed
- Nothing about the two Erdős–Graham finite-deletion questions in density 0, where they remain open.
- No claim that Theorem 1 or Theorem A is new to the literature until the world seat reports.
- The Lean file was not rebuilt here (disk guard); upstream CI built it.
