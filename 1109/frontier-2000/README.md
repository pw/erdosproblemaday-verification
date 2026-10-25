# Problem 1109 exact frontier through 2000: hostile audit

Verdict: **PASS** for the bounded exact extension, with no asymptotic claim.

Starting from the already-public exact `f(1500)=44` base, the ten further
record indices are:

```text
1509, 1535, 1595, 1707, 1735, 1779, 1835, 1919, 1991, 1999
```

Thus `f(2000)=54`. The complete primary run also starts at 1 and reproduces
all 54 transition indices. Its 201 extension decisions agree exactly with the
independent PMC audit.

The full reasoning, solver audit, source provenance, and narrow publication
scope are in `AUDIT_REPORT.md`. `BASE_DEPENDENCY.md` identifies the public
through-1500 bundle and its manifest.

Run the default frozen-artifact reproduction, which does not rerun a long
solver:

```sh
./reproduce_1109_2000_quick.sh
```

When the public base bundle is not present at `../frontier-1500`, reverify it
explicitly with:

```sh
./reproduce_1109_2000_quick.sh --base-dir PATH/TO/frontier-1500
```

`MANIFEST.sha256` covers every frozen file except itself. `KEY_INPUTS.sha256`
separately pins the load-bearing sources, binaries, transcripts, literature
snapshot, OEIS snapshots, and base manifest identity.
