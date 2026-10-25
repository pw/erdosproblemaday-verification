# Hostile independent audit: Erdos problem 1106 finite certificate

Frozen 2026-08-11 UTC. Verdict: **PASS**.

Audited bundle:

`/home/exedev/erdos_scratch/erdos1106_frontier_10100_20260811`

This verdict is for the finite certificate only. It is not an endorsement of
an exact value of `F(n)` after 116, an eventual result, either asymptotic
question, or an absolute novelty claim.

## Claims that pass

Let `p(n)` be the partition number and let `F(n)` count the distinct prime
divisors of `p(1) p(2) ... p(n)`. The audit independently verifies:

* `F(115) = 115` exactly;
* `F(116) = 117` exactly; and
* `F(n) >= n + 1`, hence `F(n) > n`, for every integer
  `116 <= n <= 10100`.

Only the first two statements are exact values of `F`. For `117 <= n <=
10100`, the result is a lower bound.

## Frozen-input and author-reproduction checks

The author's `SHA256SUMS` has SHA-256

`9986a3ddf33382f5250c5e54c1916eac7f329301ba6cfd5f958aea6e03ede2a8`.

All 23 listed files passed `sha256sum -c`. The unmodified author reproducer
then passed in 19.74 seconds and printed 9,984 successful PARI primality
decisions, 10,101 final exhibited primes, and `ALL CHECKS PASSED`. See
`author_manifest_check.log` and `author_reproduce.log`.

## Decorrelated mathematical audit

`audit_1106.py` does not import or execute the author's verifier and does not
use its Euler generalized-pentagonal recurrence. It parses only the frozen
tables after checking the author's whole manifest, then generates a PARI/GP
audit using the built-in exact `numbpart` implementation.

For every `1 <= n <= 116`, PARI independently computed `p(n)`, factored it,
proved every returned factor prime with rigorous `isprime`, and recomposed the
factorization to exactly `p(n)`. Taking unions produced 115 distinct primes
through 115 and 117 through 116. The two primes first added at 116 are 157 and
7823.

A second base engine used coefficient dynamic programming for
`product_(k>=1) (1-x^k)^(-1)`, not the pentagonal recurrence, followed by
SymPy `factorint` and `isprime`. It matched all 116 PARI partition values and
both complete PARI prime sets exactly.

The witness inputs contain one row at every index `117,...,10100`, exactly
9,984 rows. Their `(n,q_n)` digest is

`8be6ca45b91f080164c979e8b60654c01820a24276a0f4ec683e340483683f93`.

For every row, PARI checked independently that:

1. the index is the required next contiguous index and `q_n > 1`;
2. `q_n` is absent from the complete 117-prime base set and every earlier
   witness;
3. `numbpart(n) mod q_n = 0`; and
4. `isprime(q_n) = 1`.

After inserting each witness, the audit required the running exhibited-prime
count to equal `n+1`. It ended with 10,101 distinct exhibited primes at
`n=10100`. The complete base factorizations and checkpoint output are frozen
in `independent_audit_run.log` (18.45 seconds, 78,072 KB).

The deduction is immediate but important: at `n=116` the complete base gives
117 primes. By stage `n >= 117`, the certificate has added the `n-116`
pairwise distinct fresh primes `q_117,...,q_n`, each dividing the product by
its own divisibility check. Thus it exhibits

`117 + (n - 116) = n + 1`

distinct prime divisors of the product through `p(n)` at every intermediate
stage.

## Claim-boundary audit

The author consistently labels exact values only at 115 and 116. All later
statements are lower bounds. The report explicitly says it does not compute
exact `F(n)` after 116, does not prove `F(n) > n` eventually, and does not
change problem 1106's open status. `claim_boundary_scan.log` freezes the
relevant lines.

The audit deliberately does not prove that an OEIS A194261 witness is the
*smallest* new prime, nor does it refactor every `p(n)` through 10,000 to
recheck OEIS's exact `F(n)` table. Neither fact is needed: the finite proof
uses only one proven fresh divisor at each later index. FactorDB labels and
the author's saved extension partition values are likewise outside the trust
base.

## Provenance audit

An independent live browser fetch on 2026-08-11 found problem 1106 OPEN,
last edited 2025-11-16, with zero comments, zero claimed proofs, and no
current workers. The page records the known `F(n) -> infinity` and
`F(n) >> log n` results while retaining the eventual `F(n) > n` question.
See `live_1106_independent_20260811.txt`.

Current OEIS A194259 and A194261 b-files were downloaded independently on the
same date. Both are byte-identical to the author's copies and end at exactly
10,000 rows. A194259 describes `F(n) > n` after 115 as something that
"appears" to hold and links only a 1..10,000 table; A194261 likewise links a
1..10,000 table. A194260 also labels positivity after 115 as an appearance.
See `oeis_download_audit.log` and the two `current_b*.txt` files.

A strict raw-text scan of the current local site's `src/index.js` and
`src/ledger_data.js` found no `#1106`, problem URL, dedicated numeric entry,
or A194259/A194260/A194261 reference. The exact audited file hashes and dirty
worktree state are frozen in `site_provenance_audit.log`; no site file was
modified by this audit. Current upstream problem data at commit
`6929b78952e18c11d5cb28fe9438081ee1d49448` also marks 1106 open.

Targeted live searches for the eventual-inequality phrase, `A194261` with
`10100`, the first extension witness, and the 10,000-table wording found the
problem/OEIS records or unrelated partition material, but no public 10,100
extension. This supports only the author's conservative formulation: new
relative to the dated live problem page, OEIS records, and these exact
searches. It is not an exhaustive literature novelty proof.

The frozen primary texts agree with the historical context: Cilleruelo-Luca
restate that the distinct-prime count tends to infinity and give the
Schinzel-Wirsing logarithmic lower bound; Ono supplies fixed-prime
divisibility context. These asymptotic results are not used by the finite
certificate. See `primary_source_audit.log`.

## Residual trust

The result ultimately trusts exact integer arithmetic and the implementations
of PARI/GP 2.15.4 and, for a redundant small-base crosscheck only, SymPy
1.14.0. PARI's official manual states that `isprime` rigorously proves or
disproves primality and distinguishes it from `ispseudoprime`. The novelty
audit remains scoped rather than absolute. Neither residual point creates a
gap in the stated finite mathematical certificate.

