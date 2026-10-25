# Provenance and scope

All computation occurred on 2026-08-11 UTC.

- Erdős Problem 156: <https://www.erdosproblems.com/156>
- OEIS A382397: <https://oeis.org/A382397>
- Existing site verification through 102:
  `ErdosProblemADay/verification/156/extension_96_102/`

The site already carried a multi-round attempt at Problem 156 and a frozen
proof of the exact values through 102. This bundle is a continuation of that
same finite computation, not a newly untouched target and not asymptotic
progress. The live OEIS table stopped at 65 when checked earlier the same day;
the public site had already extended it through 102 before this run.

`verify_size6_sums.cpp` is copied byte-for-byte from the prior max-101 bundle
and is compiled here with a larger bound. The other three exhaustive engines
and both Python checkers were written for this extension. The deterministic
seeded search is included only to record how the eight-mark ruler was found;
the proof uses the direct witness checker, not the heuristic search.

The reported new rows are precisely `a(103)=...=a(136)=8`. The already
published `a(102)=8` is repeated only to state the contiguous theorem cleanly.
