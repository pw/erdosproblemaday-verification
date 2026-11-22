# Erdős #700(b) — Adam Tresmontant's elementary proof (submission yzwb6a, 21 Nov 2026)

f(n) = min over 1 < k ≤ n/2 of gcd(n, C(n,k)). Part (b): are there infinitely many composite n with f(n) > √n?

**Claim:** if p < q < r are primes with d = q − p < h = r − q and 2e² < p (e = r − p), then f(pqr) > √(pqr); such
triples exist in every [x, 2x) for large x (pigeonhole on primes in a short interval + Chebyshev). Full text:
`submission_yzwb6a_body.txt`.

**Verdict: VERIFIED** (22 Nov 2026). Every step holds as written (checked line by line; hostile referee: see below).

**Second instrument.** `python3 check700.py PMAX` (written here from scratch):
- brute force over EVERY k ≤ n/2 with Legendre valuations (independent of Lucas) for seven hypothesis triples from
  101·103·107 to 347·349·353: f(n) = pq > √n each time;
- brute force vs the Lucas digit test on all 5,161 triples of odd primes below 140 with r < pq (any gaps): 0 disagreements.
  (A first version without the r < pq restriction disagreed on 70 triples, all with r > pq, where Step 1's reduction
  does not apply; the fault was the test's range, not the theorem.)
- digit test over every hypothesis triple: 2,952 with p ≤ 6000 (= the submitter's count) → `check700_6000.out`;
  24,601 with p ≤ 20,000 → `check700_20000.out`; none has f(n) ≤ √n.
- controls: 103·107·113 (breaks 2e² < p) has f = 107 < √n, as the submission says; 457·461·463 (decreasing gaps)
  has f = 457 < √n.

**Ours (elementary corollaries):** f(pqr) = pq exactly under the same hypotheses (k = r attains pq); and
#{composite n ≤ X : f(n) > √n} ≫ X^{1/3}/log X (repeat the pigeonhole lemma on disjoint triples). See the /day page.

**Hostile referee** (`referee/referee_report.md`, scripts and outputs beside it): a separate Claude instance computed f three
independent ways (math.comb, Legendre, Lucas digit sets without the proof's reduction), found f = pq for all 24,601 hypothesis
triples with p ≤ 20,000 and edge cases to n ≈ 8·10¹⁸, judged Step 1, Step 2, C1 and C2 sound (wording objections only),
found the condition 2e² < p essentially sharp (failures from 2e²/p ≈ 1.07, e.g. 11969·11971·12049), and mutation-tested
`check700.py` (loosened to 2e² < 2p it flags 270 triples, all confirmed f < √n). Its notes on this README (stale output,
the 5,161 scope, dead code) were fixed and both runs redone.

**Priority:** the yes answer was claimed earlier via Maynard (our /day/700-gcd-binomial, 24 Jul 2026; a manuscript the
erdosproblems.com page reportedly credits to GPT 5.6 Sol Pro prompted by Liam Price, per github.com/aichiwuhuarou/jsp-000570-lean).
FC issue #6704 (30 Sep) proposes marking (b) solved; declined 21 Nov for lack of an audited write-up.

`submission_yzwb6a_frozen.json` is the submission as received (contact details removed).
