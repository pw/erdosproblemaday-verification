# Erdős #51 — 2026-10-21 15:00Z erdos tick (opus 5.5, Team seat 3/yt3)

Notation. For a totient a, ℓ(a) = min{n : φ(n) = a}; R(a) = ℓ(a)/a = ∏_{r | ℓ(a)} r/(r−1).
#51 asks whether R is unbounded (an infinite set A with n_a/a → ∞ exists iff sup R = ∞, since each value is attained finitely often).
A *k-seed* (OpenAI #416 preprint, Thm 2.2) is a totient d with ℓ(d) > k·d. Seeds exist for k = 1, 2 (5888 → 11985). None for k = 3 below 1e9 (our #416 tick).
Let Q_y = {primes q > y : q − 1 is y-smooth} (y-smooth = no prime factor > y). Q_2 = Fermat primes > 2; Q_3 = Pierpont primes > 3.

## Lemma 0 (trivial preimage). If a = ∏_{p ≤ y} p^{X_p} and n_0 = ∏_{p≤y} p^{f_p} with φ(n_0) = a, then R(a) ≤ ∏_{p≤y} p/(p−1).
In particular for a = 2^X 3^Y (X ≥ 1): φ(2^X 3^{Y+1}) = a, so R(2^X 3^Y) ≤ 3.

## Theorem 1 (barrier). Let y ≥ 2 and suppose Q_y is finite. Put n_K = ∏_{p ≤ y} p^K and a_K = φ(n_K).
Then for all K > 1 + max_{p ≤ y} S_p, where S_p = Σ_{r ≤ y prime} v_p(r−1) + Σ_{q ∈ Q_y} v_p(q−1),
ℓ(a_K) is divisible by every prime p ≤ y, hence R(a_K) ≥ ∏_{p≤y} p/(p−1) (and by Lemma 0, = it... ≤ it).
Proof. Let m = ℓ(a_K). Every prime r | m satisfies r − 1 | φ(m) = a_K, so r − 1 is y-smooth: r ≤ y or r ∈ Q_y.
If some p ≤ y does not divide m, then v_p(φ(m)) = Σ_{r | m} v_p(r − 1) (the factors r^{f−1} of φ(r^f) are prime to p),
which is ≤ S_p. But v_p(a_K) ≥ K − 1 because p^{K−1} | φ(p^K) | a_K. So K − 1 ≤ S_p. ∎
(Note: R(a_K) ≥ ∏ uses m/φ(m) = ∏_{r|m} r/(r−1) ≥ ∏_{p≤y} p/(p−1) once every p ≤ y divides m.)

## Corollaries (contrapositives)
C1. If sup R < ∞, then Q_y is infinite for every y with ∏_{p ≤ y} p/(p−1) > sup R. So a NO answer to #51 implies:
    for some fixed y there are infinitely many primes p with p − 1 y-smooth (open for every fixed y, as far as we know —
    for y = 2 this is the Fermat-prime question, for y = 3 the Pierpont-prime question).
C2. (k = 3.) ∏_{p ≤ 5} p/(p−1) = 15/4 > 3. If no 3-seed exists (ℓ(d) ≤ 3d for all d), then there are infinitely many
    primes of the form 2^α 3^β 5^γ + 1 (with γ... any; i.e. Q_5 infinite). Equivalently: if Q_5 is finite, a 3-seed exists
    (indeed R(a_K) ≥ 15/4 for all large K).
C3. (y = 3, the exact borderline.) For a = 2^K 3^{K−1} = φ(2^K 3^K): R ≤ 3 always (Lemma 0), and if R(2^K 3^{K−1}) < 3 for
    infinitely many K then there are infinitely many Pierpont primes. [Proof: as in Thm 1 along that subsequence — the missed
    prime p ∈ {2,3} needs Σ_{q ∈ Q_3 ∪ {small}} v_p(q−1) ≥ K − 1 − O(1) over primes q ≤ a_K + 1.]
    Our exact DP: R(2^X 3^Y) ≤ 2 + 10^−19 for every Y ≥ 1, X ≤ 120, Y ≤ 80 (so the bound 3 is never approached there).
C4. In general: no k-seed ⇒ Q_y infinite for the least y with ∏_{p≤y} p/(p−1) > k (k=2: y=3 gives 3 > 2 — vacuous since 2-seeds exist;
    k=3: y=5; k=4: y=7 (4.375); k=5: y=13? ∏ to 11 = 4.8125, to 13 = 5.2135 ⇒ y = 13).

## Where this sits
- NO direction (sup R < ∞) ⇒ infinitude of smooth-shifted primes for a fixed y (Thm 1). So proving NO is at least as hard as that
  open problem — the precise form of Tao's "very difficult with current technology" (forum, 10 Aug 2025).
- YES direction needs, for each y, exponent vectors where every cover by smooth-shifted primes is blocked — a statement about
  compositeness in a multi-parameter family (covering-congruence type, cf. #203). Thm 1 gives YES only under "Q_y finite ∀y", believed false.
- Decomposition R = T·W: T = 2 if 4 | ℓ, else ∏ over Fermat primes dividing ℓ exactly once (< 2, since ∏_s (1 + 2^{−2^s}) < 2);
  W = the rest. If 4 | ℓ no Fermat prime divides ℓ exactly once (swap 2^e·F_s → 2^{e+2^s}, smaller). So T ≤ 2 and #51 ⇔ W unbounded.
