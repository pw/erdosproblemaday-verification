# Erdos Problem 1117: frozen scout bundle

Date: 2026-08-11 UTC

Verdict: **PASS, narrow partial scope only.** The defining angular
maximum-modulus-point counting framework was absent from the frozen site files,
and the live page was OPEN with zero proof claims and no current worker. The
bundle records:

1. a current literature update: Theorem 1.1 of arXiv:2607.09462v1 gives a
   finite-order Eremenko-Lyubich class-B example with unbounded `limsup v_f(r)`;
2. an elementary sharp polynomial theorem: if the nonzero exponents of a
   non-monomial polynomial run from `m` to `d`, then `v_p(r) <= d-m` for every
   `r>0`, with equality for every radius for a two-term polynomial.

The `liminf` question remains OPEN. Nothing here solves full Problem 1117, and
no novelty claim is made for the polynomial observation.

Run the frozen checks with:

```bash
./run_all.sh
```

See `REPORT.md` for the proof, provenance audit, adjacency disclosure, and
publication-safe scope.
