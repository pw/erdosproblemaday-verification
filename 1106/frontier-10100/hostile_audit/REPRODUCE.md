# Reproduction

Prerequisites: Python 3, SymPy, PARI/GP (`gp`), GNU `sha256sum`, and GNU
`time`.

Run from this directory:

```sh
./reproduce.sh
```

The script first checks every frozen audit artifact against `SHA256SUMS` and
then reruns `audit_1106.py`. A successful run ends with both `GP_AUDIT_PASS`
and `INDEPENDENT_AUDIT_PASS`.

The verifier also checks the author's frozen manifest hash and all 23 author
bundle files before doing mathematics. It references the author bundle at:

`/home/exedev/erdos_scratch/erdos1106_frontier_10100_20260811`

The independent run uses PARI `numbpart` for every partition value through
10,100, PARI `isprime` for all 9,984 later witnesses and every base factor,
and a separate coefficient-DP/SymPy check of the complete base window.

