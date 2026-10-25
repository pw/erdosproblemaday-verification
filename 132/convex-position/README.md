# Problem 132: the convex-position theorem

This package audits the following published partial result:

> Every convexly positioned planar set of `n >= 5` points determines a
> non-diameter distance occurring among at least one and at most `n`
> unordered pairs.

The theorem is Clemen--Dumitrescu--Liu, Theorem 1.2. It proves the first part
of Problem 132 for convex point sets only. Arbitrary planar point sets and the
stronger growth question remain open.

- `public/` contains a proof reconstruction, exact arithmetic and cyclic-model
  checker, controlled negative tests, and source URLs, hashes, locators, and
  license notes. It intentionally contains no third-party source bytes or site
  snapshots. Its manifest SHA-256 is
  `9af6dabf0ffcf8d86ee3176c9bd7d875e18f9b341fda6e1aa126f04cfbd43db5`.
- `hostile_audit/` contains the independent proof, source, scope, license, and
  public-package audits. Its manifest SHA-256 is
  `510b1e755c550c9d07d06038591557eb35a5e3b23e4f688ac24d86da2f36eae6`.

Run `./reproduce.sh` to check both complete manifests and replay both public
verification suites.
