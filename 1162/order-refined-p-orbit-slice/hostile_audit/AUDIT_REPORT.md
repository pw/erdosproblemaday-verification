# Hostile audit: Erdos problem 1162 corrected v2

Audit date: 2026-08-11 UTC

Audited object:

`/home/exedev/erdos_scratch/fresh8_erdos1162_20260811_v2`

Author-bundle identity:

- `SHA256SUMS`: `bf38c14f6d43985c6b1cc36607b8ed625e9c4cfe5213bb94e57f1759bf00245c`
- `REPORT.md`: `c102e4888da8573778fb4f2ed81c0c4a63696552c26621e63d32aa19dc103c00`
- `reproduce.sh`: `514ff3537c51796c39d140ee6dd9c150f6ccfd82bbd924629387b9235a2e5de3`

## Verdict

**PASS**, as a rigorously scoped partial result.

I reconstructed the classification and count without trusting the author code,
checked the cited primary source independently, derived every asymptotic term
and sign, and wrote a separate finite verifier. I found no mathematical gap in
equations (1)--(5).

There is one publication-time packaging caveat, not a mathematical gap. The
author's `reproduce.sh` runs `audit_site_gate.py`, which asserts that the site
does not yet mention problem 1162. That assertion is correct before publication
and necessarily becomes false after publication. Preserve the author bundle for
its frozen identity, but a published root reproducer must run the theorem
verifiers directly and treat the site-gate log as a prepublication record.

## 1. Classification rebuilt from the definition

Fix a prime `p`. Suppose `H <= S_n` is a p-group with `m` nontrivial
orbits, all of size `p`, and `q=n-pm` fixed points.

On a nontrivial orbit `Omega_i`, the image `P_i=H^Omega_i` is a transitive
p-subgroup of `S_p`. Transitivity makes its order divisible by `p`, while the
p-part of `p!` is exactly `p`. Therefore `P_i` has order `p` and is a regular
cyclic group `C_p`.

The action of `H` on the union of the nontrivial orbits is faithful: an element
in its kernel fixes those points and also fixes the `q` fixed points, hence is
the identity in `S_n`. Thus

`H -> P_1 x ... x P_m = C_p^m`

is injective. Its projection to each factor is all of `P_i`, by the definition
of `P_i`. After any choice of coordinate generators, `H` is therefore an
`r`-dimensional subspace of `F_p^m` that is contained in no coordinate
hyperplane. Conversely, every such full-support subspace acts with exactly the
given p-point orbits and fixed points. This is a bijection, not just a bound.

The ambient product is recoverable from `H`. Its blocks are the nontrivial
point-orbits of `H`, and its factor on a block is the projected permutation
group `H^Omega_i`. Consequently, two different orbit frameworks cannot count
the same subgroup. Choosing different generators for the cyclic factors only
changes coordinates in `F_p^m`; it permutes the set of subspaces and creates no
extra multiplicity.

## 2. Exact count and integrality

The number of r-spaces of `F_p^m` contained in none of the coordinate
hyperplanes is, by ordinary inclusion-exclusion,

`F_p(m,r) = sum_{j=0}^m (-1)^j C(m,j) [m-j choose r]_p`.

For the orbit framework:

1. choose the fixed points and partition the others into `m` unordered
   p-element blocks;
2. on each block choose a regular cyclic subgroup of `S_p`.

A p-set has `(p-1)!` p-cycles, and each cyclic subgroup has `p-1` generators,
so it has `(p-2)!` regular cyclic subgroups. The framework count is therefore

`n! / (q! (p!)^m m!) * ((p-2)!)^m`

which simplifies to

`n! / (q! m! [p(p-1)]^m)`.

Multiplying the two independently derived factors gives exactly the author's
equation (1). Integrality and nonnegativity follow directly from the two finite
sets in the bijection; no unexplained divisibility of an alternating sum is
being assumed.

## 3. Middle-rank asymptotics

For `r=floor(m/2)`, a union bound over the coordinate hyperplanes gives

`1-F_p(m,r)/[m choose r]_p <= m [m-1 choose r]_p/[m choose r]_p`

and the Gaussian-binomial ratio on the right is

`m (p^(m-r)-1)/(p^m-1) = o(1)`.

The product formula is

`[m choose r]_p = p^(r(m-r))`

times a quotient of products of `(1-p^(-i))`. At middle rank that quotient
converges to the positive constant
`1/prod_{i>=1}(1-p^(-i))`. Hence

`log_2 F_p(m,floor(m/2)) = (log_2 p) m^2/4 + O_p(1)`.

The parity loss when `m` is odd is exactly `(log_2 p)/4`, so it belongs in the
bounded term.

When `p` divides `n`, put `m=n/p` and `q=0`. Applying base-2 Stirling to the
framework factor gives

`log_2(n!) - log_2(m!) - m log_2(p(p-1))`.

Substituting `m=n/p`, the `+(n/p) log_2 p` from `-m log_2 m` cancels the
`-(n/p) log_2 p` from the last term. What remains is

`(1-1/p)n log_2 n`

`- [(1-1/p)log_2 e + (1/p)log_2(p-1)]n + O_p(1)`.

Adding the middle-rank term gives equation (2), with a positive quadratic
term, a positive `n log n` term, and the displayed negative linear correction.

At `p=2`, the coefficients become `1/16`, `1/2`, and
`-(1/2)log_2 e`; the `log_2(p-1)` term vanishes. Also
`r=floor(m/2)=floor(n/4)`, so equation (3) counts subgroups of the single exact
order claimed. The independent integer calculation at `n=20` is

`52,502,131,339,708,050`.

## 4. Rank-limit laws

The framework factor is independent of rank, so uniform choice from the whole
slice reduces exactly to uniform choice among full-support subspaces.

For `m=2s`, write `r=s+k`. Then

`r(m-r)=s^2-k^2`,

which gives the limiting relative weight `p^(-k^2)`. For `m=2s+1` and
`r=s+k`,

`r(m-r)=s(s+1)-k(k-1)`,

which gives `p^(-k(k-1))` and the two equal central modes `k=0,1`.

For every fixed `k`, the preceding hyperplane bound makes full support have
probability `1-o(1)`. Uniformly in `r`,

`[m choose r]_p <= p^(r(m-r))/prod_{i>=1}(1-p^(-i))`.

After division by the central exponent, this supplies the summable majorants
`C_p p^(-k^2)` and `C_p p^(-k(k-1))`. Dominated convergence justifies both
normalizing theta sums and proves equations (4) and (5), including the signs
and parity shift. Tightness gives `R_m=m/2+O_Pr(1)`.

## 5. Independent finite verification

`independent_verify.py` imports no author code. It performs the following
separate checks.

- It enumerates all subspaces of small `F_p^m` by additive closure, not RREF,
  and matches both Gaussian-binomial and inclusion-exclusion counts.
- It constructs the complete subgroup lattice of `S_5` directly from the 120
  permutations. The resulting 156 subgroups match OEIS and every eligible
  p-orbit slice matches equation (1) for `p=2,3,5`.
- It enumerates every orbit framework and actual permutation subgroup for the
  full-support slices in `S_8` at `p=2` and `S_9` at `p=3`. It checks the
  actual point-orbits, recovers each coordinate projection, and rejects any
  collision between frameworks.
- It checks exact arithmetic and nonnegativity for five primes, independently
  obtains the `n=20` integer, checks bounded residuals after every term of
  equation (2), and checks both parity-dependent theta ratios.

The direct permutation totals include:

- `S_8, p=2`: 105 frameworks and rank counts
  `{1:105, 2:1365, 3:1155, 4:105}`;
- `S_9, p=3`: 280 frameworks and rank counts
  `{1:1120, 2:2800, 3:280}`.

The independent run ends with
`INDEPENDENT PROBLEM 1162 FINITE AUDIT PASSED`.

The author's frozen `./reproduce.sh` also passed in full before publication,
including its manifest, RREF checks, separate permutation construction, and
asymptotic audit.

## 6. Primary sources, site gate, and provenance

I fetched the official arXiv source and PDF independently. Their SHA-256
digests exactly match the bundle copies. The source states Theorem 1's
`2^(n^2/16+o(n^2))` result, Theorem 6's Sylow-order statement, and Proposition
7.3's lower-bound construction from subdirect products of disjoint p-cycles.
The new formula is an exact order refinement of that construction, not a new
proof of the global leading exponent.

An independent Bright Data fetch of the live problem page confirmed the
statement, OPEN status, zero comments, zero claimed proofs, no listed worker,
and the 2026-01-23 edit date. Independent local searches found no standalone
`1162` or same-topic phrase in either site source file. Before publication,
`https://erdosproblemaday.com/report/1162` returned HTTP 404.

The 38 MB `parallel_sn_19.tar.xz` file is not an input to any theorem or finite
check. It concerns conjugacy classes, not labelled subgroup totals. It may be
omitted from a lean publication bundle as long as that omission is explicit;
doing so changes the author manifest identity, so the frozen original should
remain archived separately.

## 7. Scope audit

The report correctly labels the result **PARTIAL**. It does not determine
`f(19)`, improve the known global leading exponent, prove a global second-order
upper bound, or give the order law of a uniformly random subgroup of `S_n`.
The theta laws concern only the explicitly defined p-orbit slice. A literature
search miss cannot certify novelty, and the report appropriately avoids such a
claim.

Within that narrow scope, the exact theorem, the one-order lower bound, and the
restricted statistical law are rigorous.
