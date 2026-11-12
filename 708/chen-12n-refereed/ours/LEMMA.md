# Erdős #708 — the K_{2,t} placement exists for every t (our lemma, 2026-11-12)

Notation (Chen's): for A = {a_1<…<a_n} ⊂ ℕ_{≥2}, m = max A, x ≥ 0, I = {x+1,…,x+m},
g(A,x) = min{|B| : B ⊆ I, ∏A | ∏B}; g(n) = sup over |A| = n, x ≥ 0.

**Lemma (placement).** Let t ≥ 2 and primes w_1 < … < w_t < q_u < q_v satisfy
 (P1) m := w_t q_v < 2 w_1 w_2,
 (P2) q_u² ≥ m + q_u.
Put A = {w_i q_u, w_i q_v : 1 ≤ i ≤ t} (|A| = 2t, max A = m) and A⁺ = A ∪ {q_u} (|A⁺| = 2t+1, max A⁺ = m).
Then there is x ≥ 0 with g(A,x) ≥ 3t−1 and g(A⁺,x) ≥ 3t (equality in both; see the end).

**Construction of x.** Let Π = w_1⋯w_t q_u q_v and a = −⌊m/2⌋; the window will be {u+a, …, u+a+m−1}.
(P2) gives q_u² > m, and q_v² > q_u²; so a window of length m meets at most one multiple of each q². For q ∈ {q_u, q_v} let C_q = {a+m, …, a+q²−1} (mod q²): q²−m consecutive residues. For q_u this is ≥ q_u by (P2);
for q_v, q_v² − m = q_v(q_v − w_t) ≥ 2q_v. So C_q contains a multiple q·s_q of q; s_q ≢ 0 (mod q), because the
residue 0 = offset of u lies in {a,…,a+m−1}, outside C_q. By CRT choose k ≥ 1 with
 k ≡ −s_q·(Π/q)^{−1} (mod q) for q ∈ {q_u,q_v}, and k ≢ 0 (mod w_i) for every i.
Set u = kΠ and x = u + a − 1 ≥ 0, so I = {u+a, …, u+a+m−1} and u ∈ I.

**Facts.**
 (F1) v_p(u) = 1 for every prime p ∈ D := {w_1,…,w_t,q_u,q_v} (k is prime to every p ∈ D; k ≢ 0 mod q since s_q ≢ 0).
 (F2) No b ∈ I∖{u} is divisible by two distinct primes of D: if p ≠ p' in D divide b then pp' | b−u, but
      0 < |b−u| ≤ ⌊m/2⌋ < w_1w_2 ≤ pp' by (P1).
 (F3) No b ∈ I is divisible by q_u² or q_v²: q² | u+δ ⇔ δ ≡ −kΠ ≡ q·s_q (mod q²) (as −k·Π/q ≡ s_q mod q),
      and q·s_q mod q² lies in C_q, which is disjoint from the offsets {a,…,a+m−1}.

**Lower bound for A.** Demands: v_{w_i}(∏A) = 2, v_{q_u}(∏A) = v_{q_v}(∏A) = t. Let B ⊆ I with ∏A | ∏B.
By (F2) each b ∈ B∖{u} is divisible by at most one prime of D, and by (F3) a b divisible by q contributes exactly 1 to v_q.
 - If u ∈ B: u gives 1 to each prime (F1). q_u needs ≥ t−1 further elements, q_v ≥ t−1 further, each w_i ≥ 1 further,
   and these sets are pairwise disjoint (F2): |B| ≥ 1 + 2(t−1) + t = 3t−1.
 - If u ∉ B: q_u needs ≥ t elements, q_v ≥ t, each w_i ≥ 1, pairwise disjoint: |B| ≥ 3t.
Hence g(A,x) ≥ 3t−1. For A⁺ the demand of q_u is t+1, adding one element in both cases: g(A⁺,x) ≥ 3t.

**Equality (not needed for the theorem).** I contains ≥ ⌊m/q_u⌋ ≥ w_t ≥ t+1 multiples of q_u, ≥ ⌊m/q_v⌋ = w_t ≥ t+1
multiples of q_v and ≥ ⌊m/w_i⌋ ≥ q_v ≥ 2 multiples of each w_i, so u plus t−1 (resp. t) other multiples of q_u,
t−1 other multiples of q_v and one other multiple of each w_i is a cover of size 3t−1 (resp. 3t).

**Theorem.** g(n) ≥ ⌊3n/2⌋ − 1 for every n ≥ 4.
Proof: n = 2t or 2t+1 with t ≥ 2; apply the Lemma. Primes satisfying (P1),(P2) exist for every t: by the prime number
theorem, for X large there are ≥ t primes in [X, 1.2X) (take w_1,…,w_t the first t of them) and ≥ 2 primes
q_u < q_v in [1.3X, 1.32X). Then m = w_t q_v < 1.584X² < 2X² ≤ 2w_1w_2 (P1), and m + q_u < 1.584X² + 1.32X ≤ 1.69X²
≤ q_u² for X ≥ 13 (P2). Label: (b) rigorous, using the prime number theorem (a theorem, so unconditional); for t ≤ 14 the explicit primes in
k2t2_run.log make it (a)+(d) unconditional (each instance also solved exactly by exact.py).

**Context.** Chen's paper (sec_remains, Prop. "sharpness") proves g(A,x) = 3t−1 on K_{2,t} *provided* a window can be
placed so that M = Π is its only two-prime element and no q² has a multiple in it, exhibits placements for t = 2..6,
and says the coefficient of β in g(A,x) ≤ n+β "cannot be so replaced at all if the placement exists for every t —
which we have not proved". Chen's literal hypothesis puts the special integer at M = Π; we do NOT show a window around Π itself works for every t.
His count goes through verbatim for u = kΠ with gcd(k, Π) = 1, and the lemma gives such a window for every t, so his
conclusion about the β coefficient follows. Centring on a common multiple with each prime once is the 1959 device;
choosing k to clear the q²-multiples is the only new step. Credit: the referee in Chen's pipeline (run37, §C.3) asserted
'refuted for every θ < 1' without proof. Ratio 3/2 − 1/n ≤ (2−o(1)) of Erdős–Surányi asymptotically; the point
is an explicit bound at every n and the closing of Chen's hypothesis, not a better asymptotic.
