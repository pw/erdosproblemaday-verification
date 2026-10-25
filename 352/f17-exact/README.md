# Erdős 352 / Koizumi lattice model: exact `f(17)=32`

This directory is a self-contained computational certificate for the finite
statement

```text
f(17) = 32
```

where `f(N)` is the largest cardinality of a finite `N`-avoiding subset of
`Z^2`: every triple `p,q,r`, with repetitions allowed, must satisfy

```text
|area(p,q,r) - N| > diameter(p,q,r).
```

This is a rigorous finite result in Koizumi's lattice model. It does **not**
prove the uniform estimate `f(N)=O(N)` and therefore does not solve the
original continuous Erdős problem 352.

## Files

- `erdos352_n17_verify.py`: full standalone checker. It verifies the
  32-point witness, exhausts all 125 normalized diameter cases and all 9,414
  fixed-high branches, audits every coloring certificate through independent
  arithmetic, and applies the matching refinement to the sole exceptional
  branch.
- `erdos352_n17_matching_audit.py`: short independent reconstruction of the
  exceptional `B=(5,4)` branch and its 512-choice matching certificate. It
  also verifies the witness.
- `full_n17_output.txt`: complete output and `/usr/bin/time` measurement from
  the final full run.
- `focused_audit_output.txt`: complete output of the short matching audit.
- `reference_upper_n17.json`: output of the independent public upper-bound
  implementation at commit
  `7a4a19468771766cb4f20e10dfa5cf770cc2487b`, run with exact chromatic
  minimization disabled. It confirms that only `B=(5,4)`, no-high reaches the
  pairwise relaxation 33; every other diameter case is at most 32.
- `REFERENCE_CHECKS.md`: independent-source, timing, and live-page details.
- `REPORT.md`: human-readable site report for the new finite result.
- `hostile_audit/`: an independent full reconstruction using different
  geometry and DSATUR code, a strict-predicate boundary audit, and the exact
  producer version it audited.
- `SHA256SUMS`: frozen artifact hashes.

## Reproduce

From this directory, with Python 3.10 or newer:

```bash
python3 erdos352_n17_matching_audit.py
python3 erdos352_n17_verify.py --min-n 17 --max-n 17 --json
python3 hostile_audit/audit_exception_5_4.py
python3 hostile_audit/audit_strict_predicate.py
python3 hostile_audit/audit_352_n17.py
sha256sum -c SHA256SUMS
```

Only the Python standard library is required. On the exe.dev VM, the focused
audit took 0.09 seconds and the full exhaustive run took 113.40 seconds with
20,292 KiB maximum resident memory.

The primary and focused checkers deliberately use Python assertions as
fail-closed checks. Run them with ordinary `python3`; `python3 -O` is not a
certified invocation.

The canonical full-certificate stream digest printed by the primary checker is

```text
dd1b957a56174169a95cc31fd68d77b47d51dd38745f6252059954b74aad78e2
```

The hostile full reconstruction independently prints global cap 32 and the
branch-manifest digest
`0a8e0e483ec7e279d3099d5689cb1b32c9b4d5ea5f3b57d0283dfa3302613fae`.
Its detailed verdict and frozen measurements are in
`hostile_audit/AUDIT_REPORT.md` and `hostile_audit/AUDIT_LOG.txt`.

## Certificate in one paragraph

The witness has 32 distinct points and all 5,984 triples have positive exact
integer gap, with minimum 5. The diameter-pair reduction produces 125 cases;
9,539 coloring certificates cover their no-high and fixed-high branches.
Every branch is bounded by 32 except the pairwise relaxation for `B=(5,4)`,
whose no-high pool has 40 vertices. Its incompatibility graph has 48 edges and
contains a displayed matching of size 9. A compatible 31-subset would have to
omit exactly one endpoint of each matching edge, so there are only `2^9=512`
possibilities. Exactly two omissions cover all 48 incompatibility edges; each
remaining 31-set contains one forbidden triple, of exact gap `-4`. Hence that
branch has at most 30 candidates, or 32 points including the diameter pair.

## Provenance

The 32-point lower witness was posted previously by BorisAlexeev and appears
in KentaKitamura's public witness repository. The new contribution certified
here is the exhaustive upper bound at `N=17`; no priority claim is made for
the witness.
