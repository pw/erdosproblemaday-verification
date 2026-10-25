# Problem 1162: an order-refined p-orbit slice

This directory proves an exact formula for a natural family of p-subgroups of
the symmetric group, refines the known lower-bound construction at one exact
order, and gives the order distribution inside that family.

For a prime `p`, write `n=pm+q`. Let `T_p(n;m,r)` count p-subgroups of `S_n`
with exactly `m` nontrivial orbits of size `p`, `q` fixed points, and order
`p^r`. The author report proves

```text
T_p(n;m,r) = n! / (q! m! [p(p-1)]^m)
             * sum_{j=0}^m (-1)^j C(m,j) {m-j choose r}_p.
```

Here `{d choose r}_p` is a Gaussian binomial coefficient. In particular, for
even `n`, the single order `2^floor(n/4)` contains

```text
2^(n^2/16 + (n/2)log_2(n) - (n/2)log_2(e) + O(1))
```

members of this family. The report also proves parity-dependent discrete theta
limit laws for the order within the same restricted family.

- `author/` is the corrected v2 bundle. Its manifest hash is
  `bf38c14f6d43985c6b1cc36607b8ed625e9c4cfe5213bb94e57f1759bf00245c`.
- `hostile_audit/` independently rebuilds the classification, count,
  asymptotics, and finite checks. Its manifest hash is
  `fee79692aa8ea284263f9fba222efaaa2a6e04e9c5b870c8ae839f5c2d586072`.

The immutable author manifest also names `parallel_sn_19.tar.xz`, a 38 MB
archive about conjugacy classes that is not used by the theorem or any
verifier. It is deliberately omitted from this lean publication. The root
reproducer checks the original manifest identity and every included artifact
after filtering exactly that one path.

The author's frozen `reproduce.sh` includes `audit_site_gate.py`, whose purpose
was to assert that Problem 1162 was absent before publication. That check must
fail once the result is published, so the root reproducer preserves the script
but directly runs the three mathematical author checks instead. It then runs
the hostile verifier independently.

This is a rigorously scoped partial result. It does not determine the total
number of subgroups of `S_19`, improve the known global leading exponent, give
a global second-order upper bound, or establish an order law for a uniformly
random subgroup of `S_n`.
