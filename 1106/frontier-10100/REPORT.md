# Erdos problem 1106: finite verified frontier through 10,100

Frozen on 2026-08-11 UTC. This is a finite computational result, not a
solution of either asymptotic question in problem 1106.

## Certified statement

Let `p(n)` be the integer partition function and let `F(n)` be the number of
distinct prime divisors of

    p(1) p(2) ... p(n).

The bundled verifier proves:

* `F(115) = 115` exactly.
* `F(116) = 117` exactly.
* `F(n) >= n + 1`, hence `F(n) > n`, for every integer
  `116 <= n <= 10100`.

It does not compute exact values of `F(n)` after 116. It does not prove that
`F(n) > n` eventually, and it does not change the parent problem's OPEN
status.

## Proof certificate

The verifier computes `p(0),...,p(10100)` over the integers with Euler's
generalized-pentagonal recurrence. It completely factors `p(1),...,p(116)`
by trial division. There are exactly 115 distinct factors through 115 and
exactly 117 through 116.

For each `117 <= n <= 10000`, the certificate takes one candidate divisor
from the frozen OEIS A194261 table. For each `10001 <= n <= 10100`, it takes
one divisor from `extension_witnesses_10001_10100.tsv`. The verifier does not
trust the descriptions attached to either source. It independently checks
that every candidate:

1. is greater than one;
2. divides the recomputed integer `p(n)`;
3. differs from all 117 base primes and all earlier selected candidates; and
4. is prime according to PARI/GP's rigorous `isprime`, not a probable-prime
   test.

Thus, by stage `n`, the verifier has exhibited `n+1` distinct primes dividing
the product through `p(n)`. This proves the claimed lower bound at every
intermediate index, not only at 10,100.

The passing run reports 9,984 rigorous primality decisions, a final witness
set of 10,101 primes, and these independently generated digests:

    partition-array SHA-256:
    b03896a62abd65ba378acc464f1a4215e39ccc079ad3e2b78f2e613b25f7c7d1

    witness-pairs SHA-256:
    8be6ca45b91f080164c979e8b60654c01820a24276a0f4ec683e340483683f93

## Claim boundary

OEIS A194259 already publishes exact `F(n)` values through 10,000 and says
that `F(n) > n` "appears" to hold for `n > 115`. This bundle extends only the
rigorously checkable strict-inequality frontier by 100 indices. The new part
is the lower-bound certificate for 10,001 through 10,100, not an exact
extension of A194259.

The dated live checks in `PROVENANCE.md` support only a claim relative to the
current problem page, current OEIS records, and the listed exact web searches.
They are not evidence for an absolute or exhaustive novelty claim.

## Trust base

The proof uses Python exact integer arithmetic, the elementary recurrence,
trial division for the small base window, and PARI/GP 2.15.4 `isprime` for
rigorous primality. FactorDB was used only to discover candidate factors for
the 100-index extension. The verifier neither reads nor trusts the saved
FactorDB responses or the saved extension partition values.

