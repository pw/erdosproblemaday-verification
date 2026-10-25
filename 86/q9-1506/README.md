# Problem 86: a 1506-edge C4-free subgraph of Q9

This directory certifies only

```text
ex(Q_9, C_4) >= 1506.
```

The explicit 1,506-edge subgraph improves the specifically identified public
1,505-edge certificate by one edge. It is a lower bound, not an exact value,
an optimality result, or progress on the asymptotic conjecture.

- `author/` contains the canonical graph, portable edge list, deterministic
  generator, two exhaustive verifiers, the public comparison, sources, logs,
  and provenance. Its manifest hash is
  `2878fa5ec38e7d52e056883f53dfbeb72c72a200ec6eb133402cbf620d890e3c`.
- `hostile_audit/` contains a strict independent parser, complete face and
  common-neighbour checks, a negative control, a distinct reproduced
  1,506-edge graph, current-source checks, and the audit report. Its manifest
  hash is
  `c149fc744c9eb44cde6db76d62573ebe70beb4c0bb25b65331336704c7696f52`.

The hostile audit's frozen manifest also covers a complete clone of the public
Q9-through-Q15 source repository. That redundant 52-file subtree is omitted
from this lean publication; the relevant public Q9 graph and fixed commit
metadata remain in both bundles. The root reproducer checks the original audit
manifest identity and every included artifact after filtering exactly those
52 paths.

Run `./reproduce.sh` to verify the packages, regenerate the canonical graph,
and rerun all definition-level checks.
