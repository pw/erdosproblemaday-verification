# Literature / novelty seat (Opus, web), 2026-11-09 — findings as returned (abridged)

1. Exhaustive checks: nothing peer-reviewed. Largest outside range found: an unreviewed GitHub repo
   (github.com/Ashutosh0x/jsp-000240-odd-greedy): all reduced a/b with odd b ≤ 199 (8,150 fractions, max 21 at
   191/197) + a = 2, 3 for b ≤ 10,000. OEIS A286720 b-file (2n/(2n+1), n ≤ 10,000); A069581 (small n). Eppstein 1997
   searched 3/x by residue class, not exhaustively. Our own July report: b ≤ 999.
2. 3/(N!−1), 3/(2·N!−1): no computation for N = 500 or any large N found. Pihko 2010 Thm 2.3 covers the family
   k = −1 + t·a(a+1)…(a+n) (t = 1, 2 are Brown's two forms); Thm 3.5: 2/(2(p−1)!−1) -> 2..p−1, 1 exactly.
   Brown kmath454: "limiting primes" by which a ramp must break (computed mod p).
3. Parity alternation: Pihko 2001 eq. (2.4) "a_i ≢ a_{i+1} (mod 2)" and (2.5) "h(a/b) ≡ a (mod 2)". Fixed points:
   Pihko 2010 Lemma 2.2 (k ≡ −1 preserved), proof of Thm 3.5 (k ≡ (p−1)/2, i.e. z ≡ 0, invariant), Lemma 3.1;
   Brown kmath454's d ≡ ±1. => both moved from "ours" to "credited".
4. Recent work: Louwsma–Martino, Integers 25 (2025) #A46 (two-term odd greedy expansions), arXiv 2309.07280; nothing
   new on termination. Graham 2013 survey on the squares variant. FC 282.lean lists all as open.
Sources saved by the seat in /tmp/lit282/.
