# Source provenance and audit

Sources were checked on 2026-08-11 UTC.

## Problem statement

- Live page: <https://www.erdosproblems.com/168>
- Independent formal-statement transcription:
  <https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/168.lean>
- The live page defines `F(N)` as the largest subset of `[N]` avoiding every
  `{n,2n,3n}`.  It records that Graham, Witsenhausen, and Spencer proved the
  density limit exists and gave the smooth-prefix series, and asks for its value
  and whether it is irrational.
- The page was last edited 2026-03-23.  Its discussion records Sean Eberhard's
  September 2025 computation and corrected decimal.  There were no proof claims
  and no active worker at audit time.
- The site presented a Cloudflare challenge to direct HTTP, so the public body
  and discussion were read through Bright Data's browser proxy.

## OEIS / Eberhard files

- <https://oeis.org/A057561>: `f(k)`, the maximum corner-free subset size in the
  first `k` 3-smooth numbers.
- <https://oeis.org/A004059>: first prefix index where `f(k)` reaches `n`.
- <https://oeis.org/A386439>: decimal digits of the density constant.
- Frozen files and SHA-256 values (also confirmed against the remote bytes on
  2026-08-11):

```text
bba41cd187052c20e638c539893f16f73d23956f9900caa882e06778256b15ea  b004059.txt
1e38d564f8e42ea7c26843186ca76c4077e797ebcac402a3de00b3f8df7e2529  a004059.py.txt
92b08a0c6647f55851356f6f3f6f7c8435a19446d5237c0ab0a53a9357aaa25d  a386439.py.txt
```

### A004059 code audit

`a004059.py.txt` correctly generates the increasing 3-smooth sequence, builds
all lattice points `2^x 3^y <= d_k`, adds exactly one `v[x,y]+v[x+1,y]+
v[x,y+1] <= 2` constraint per present corner, and maximizes the selected count.
The output loop correctly records the first prefix where the optimum reaches
each successive integer.  Thus its formulation and indexing match the stated
sequence.

One numerical robustness issue remains: it returns
`int(p.get_objective_value())`, which truncates the floating solver value instead
of rounding and checking integrality tolerance.  This is not evidence of an
actual wrong row, and the endpoint was independently reproduced here, but
`round` plus a tolerance assertion would be safer.

### A386439 code audit

Lines 22-24 subtract the current reciprocal term before testing whether the
index has passed the known frontier.  Consequently the `k=5001` term is missing
from the alleged upper tail.  `audit_density_interval.py` reconstructs the issue
with exact rational arithmetic and confirms that it does not alter the reported
35 common digits.

## Post-page literature

- Nikola Veselinov, *Extremal densities for forbidden configurations in
  S-smooth numbers*, arXiv:2604.15515v1, submitted 2026-04-16:
  <https://arxiv.org/abs/2604.15515>
- Frozen PDF SHA-256:
  `68e3b58de8d2bf8f4e5fb48560f2c43e489d7979e7e0f8c44ed2ddf1c7adbb14`.
- It proves `f(k)=2k/3+O(sqrt(k))` for `{2,3}`, restates the density series and
  an explicit exact tail, proves that optimal prefix sets cannot always be
  chosen nested (Proposition 6.2), and characterizes increments via the unique
  newly introduced corner (Proposition 6.3).
- It does not determine the density constant or settle irrationality.  The
  current computation is therefore not superseded by a claimed resolution, but
  its coloring mechanism and one-point increment logic are consistent with and
  partly derivative of that paper.

## Historical citation

Ronald L. Graham, H. S. Witsenhausen, and J. H. Spencer, "On extremal density
theorems for linear forms," in *Number Theory and Algebra*, Academic Press,
1977, pp. 103-109.  This is the primary historical source cited consistently by
the live page, OEIS, and Veselinov.  The present checkpoint does not re-prove its
global density decomposition.
