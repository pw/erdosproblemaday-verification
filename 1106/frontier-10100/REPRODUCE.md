# Reproduction

Prerequisites:

* Python 3 with arbitrary-precision integers (tested with Python 3.12.3)
* PARI/GP providing `gp` on `PATH` (tested with PARI/GP 2.15.4)
* GNU `sha256sum`

From this directory, run the executable reproducer:

```sh
./reproduce.sh
```

It first verifies every frozen artifact against `SHA256SUMS`, then runs:

```sh
/usr/bin/time -f 'TIME %e sec MAXRSS %M KB' \
  python3 verify_erdos1106_frontier.py
```

The proof output must include `ALL CHECKS PASSED`. `verify_run.log` records
the first frozen run (18.83 seconds, 69,780 KB maximum resident set), while
`final_verification.log` records the clean-bundle rerun (15.71 seconds,
69,464 KB). The machine is described in `environment.txt`.

The three proof inputs whose hashes are also hard-coded in the verifier are:

```text
b194259_20260811.txt
b194261_20260811.txt
extension_witnesses_10001_10100.tsv
```

`extension_partitions_10001_10100.txt` and
`factordb_extension_10001_10100.jsonl` preserve the discovery trail only.
Deleting either one does not affect verification.
