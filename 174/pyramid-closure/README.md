# Problem 174: pyramid closure

This package audits the following literature-derived partial result:

> If `B` is a finite Euclidean Ramsey set and `z` lies outside the affine
> hull of `B`, then `B union {z}` is Ramsey.

Kenneth Moore proves this in Theorem 1.2 of arXiv:2608.09649v1. It resolves
Ivan--Leader--Walters Conjecture 8 and extends their earlier subsoluble-base
case to an arbitrary Ramsey base. It does not characterize all finite
Euclidean Ramsey sets, so Problem 174 remains open.

- `public/` contains the proof reconstruction, source URLs and hashes, exact
  rational fixtures, optimization-safe verifier, and tamper harness. It
  intentionally contains no third-party PDF. Its manifest SHA-256 is
  `96d9a06c67206c4a7d22f00b41d21ead41314ecc87848e1990420ab1648ba9cf`.
- `hostile_audit/` records the final independent public-release audit. Its
  manifest SHA-256 is
  `6d38a4dfef13fd4a366f92fb45b90f440950987b45b1e590d1100288b0d4b6c7`.

Run `./reproduce.sh` to check both frozen manifests and rerun the public
package under normal Python, `-O`, and `-OO`, including all tamper controls.
