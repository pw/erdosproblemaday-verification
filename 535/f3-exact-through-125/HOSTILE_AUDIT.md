# Hostile-audit verdict

Audit date: 2026-08-12 UTC.

**PUBLISH this corrected lean bundle.**

The initial producer bundle was mathematically sound but package-blocked:
`REPORT.md` compiled onto a manifest-pinned executable, and the resulting
binary bytes depended on whether the source path was absolute or relative.
This public bundle corrects the command to compile to `/tmp/verify535` and
does not ship any executable, `__pycache__`, `.pyc`, or empty compiler log.

Independent hostile checks established all of the following:

- the original frozen 17-file manifest passed before audit;
- the Bright Data captures showed `OPEN`, zero claims, no worker,
  collaborator, or formalizer, and all nine comments were visible;
- prime-power-layer and direct-gcd definitions agreed for every distinct
  triple through 125;
- endpoint edge counts independently regenerated as 71,799, 109,838, and
  113,132;
- the three lower witnesses passed direct checks over respectively 364, 455,
  and 560 triples;
- the interval obligations exactly pair left-end witnesses with right-end
  target-plus-one UNSAT searches, proving every N from 101 through 125;
- fresh Python and independently rebuilt C++ runs reproduced all endpoint
  edge counts, node counts, and UNSAT results; and
- a third prime-power-layer formulation exhaustively enumerated every subset
  for every N through 18, obtaining
  `1,2,2,3,3,3,3,4,5,5,5,5,5,5,5,6,6,7`, while the primary solver agreed at
  both the optimum and optimum-plus-one for each N.

The audit found no arithmetic, modeling, pruning, completeness, off-by-one,
live-gate, collision, or novelty-wording defect.  The claim remains a finite
exact extension only, with no asymptotic or historical-priority claim.

Canonical witness-stream SHA-256 values from the hostile audit were:

```text
size 14: 395a7c7c91c413ef75cbdba8833a060fc5506170a3616d2dd3c05645034b7664
size 15: 3b495bace2acdf7c1a50026af89d98afe9eb0e9ad796c60c48590f4e978acd89
size 16: 97e4e75786ef57e0b226819626037550467b4145b2e010461d9c4263d0a979c0
```

The full development audit remains frozen separately at
`/tmp/erdos535_f3_exact_101_125_hostile_audit`; the lean public artifact is
self-contained and does not depend on that path.
