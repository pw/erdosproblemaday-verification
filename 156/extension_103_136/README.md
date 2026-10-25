# Problem 156: exact A382397 values through 136

This directory certifies

```text
a(n) = 8 for every 102 <= n <= 136.
```

The new sequence rows are `a(103)=...=a(136)=8`; the existing certificate
already established `a(102)=8`. This is a finite computational extension and
does not improve the asymptotic bounds in Erdos Problem 156.

- `author/` contains two complete seven-mark enumerators, complete searches
  through six marks, the explicit eight-mark ruler, direct witness checks,
  frozen outputs, and its SHA-256 manifest. Its manifest hash is
  `566ac359a544556f7453a1b02044692488ed91f0ad2eb4cc09ca24a1503ecd89`.
- `hostile_audit/` contains a third seven-mark enumerator, an independent
  one-tree search through six marks, literal insertion checks, frozen outputs,
  and the audit report. Its manifest hash is
  `bf9b305f499150f0918b48165f358442112ed37c8a6b0ac06d5cc5e13bd951fa`.

The lower-bound searches agree that every Sidon ruler with at most seven marks
and diameter at most 135 has a blocked run of length at most 101. The ruler

```text
{0,39,47,51,52,61,67,101}
```

has a blocked component of length 136, and its translations give maximal
eight-element Sidon sets for all 35 claimed values.

Run `./reproduce.sh` to verify both manifests and rerun the portable author and
hostile-audit checks.
