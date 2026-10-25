# Seat T — printed §4 (comparing products of shifted primes), §5 (uniqueness of the continuous prefix), §7 (least preimages).
Read COMMON.md first.
1. §4: the uniform sieve for two or three linear forms (uniformity in the coefficients, the singular-series bound, the dependence of
   implied constants), and the comparison estimate — every inequality chain; check exponents and that the error terms are small
   enough for the way §5 uses them (sum over all ordered pairs of prefixes, the number of layers, the bands for log log p_i).
2. §5: counting pairs (n, n') of tuples with φ(n) = φ(n') — the heart of "distinct values". Check that every collision type is
   covered (equal prefixes with different tails is ALLOWED by design; different prefixes must be rare), the costs for recovering the
   tuple data inside residual factors, and Proposition 5.3 (removal of at most a small proportion). Try to construct a family of
   collisions the argument misses (e.g. prefixes differing in many primes simultaneously, primes p with p−1 sharing large factors).
3. §7: Lemma 7.1/7.2/7.3, Theorem 2.2's two alternatives, the k = 1, 2 positivity (where exactly is k = 2 shown? exhibit the seed d
   with ℓ(d) > 2d they use, or the argument that replaces it), and the claim that 'the first alternative for every k is equivalent to
   ℓ(d)/d unbounded'. Lemma 7.2 is attributed to Ford's proof of his Theorem 2 (Ford arXiv 1104.3264 §5 pp. 24–26 eqs (5.10)–(5.19),
   §7.3 p. 39): fetch Ford and check that the construction really gives the FULL inverse fiber {b d_1, …, b d_κ} on a positive
   proportion, as used.
   Small-case numerics where the statement allows: compute ℓ(v) for all totients v ≤ 10^7 (≤ 8 GB, 2 cores) and report the fractions
   N_k(x)/V(x) for k = 1..5 at x = 10^6, 10^7, and max ℓ(d)/d for d ≤ 10^7.
Out of scope: §2–§3 and §6 — another seat; take their statements as given but say which ones you used.
