# Problem 86: a 1531-edge C4-free subgraph of Q9

This directory certifies only

```text
ex(Q_9, C_4) >= 1531.
```

The explicit graph improves this site's preceding 1,506-edge certificate by
25 edges and the specifically identified external 1,505-edge certificate by
26. It is a finite lower bound, not an exact value, an optimality result, or
progress on the asymptotic conjecture.

- `author/` contains the canonical graph, independent face and
  common-neighbour checks, controlled negative tests, predecessor graphs,
  comparison scripts, generator provenance, logs, and a complete manifest.
  Its manifest SHA-256 is
  `520b3c6ae7ced58c696dc8ccb7141e141d0e9db95bec56d1be7865353b88806f`.
- `hostile_audit/` contains a clean-room parser, exhaustive face and all-pairs
  common-neighbour checks, optimization-mode and tamper tests, frozen dated
  evidence, and the independent report. Its manifest SHA-256 is
  `70e62fe1c011767a8cd0c92437ba0319a29c56a79b7e12dd87dc9f26987b1000`.

Run `./reproduce.sh` to verify both frozen packages and rerun the complete
offline hostile audit.
