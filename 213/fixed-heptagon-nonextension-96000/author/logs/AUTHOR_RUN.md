# Author run log

Date: 2026-08-11 UTC.

Independent optimized runs (executed concurrently):

```
C++ elapsed=5.23 seconds, max RSS=3548 KiB
Go  elapsed=6.45 seconds, max RSS=7164 KiB
```

Both emitted the byte-identical summary frozen in `cpp_latest.txt` and
`go_latest.txt`:

```
triangle_pairs=1765966460
distance_bound=96000
characteristic_2002=1017
oriented_candidates=4068
degenerate_candidates=169729
extensions=0
```

The Python metric/general-position checker emitted `matrix_latest.txt`.

A full clean `./reproduce.sh`, including compilation, both sequential scans,
the Python checker, output comparison, and JSON validation, completed with
exit status 0 in 17.68 seconds on the environment in `ENVIRONMENT.md` before
the bundle was made read-only.

Additional final checks:

- `go vet verify_semiperimeter.go`: exit 0;
- `g++` with `-fsanitize=undefined`, followed by a full scan: exit 0 with the
  same summary;
- `python3 -m py_compile verify_matrix.py`: exit 0;
- `shellcheck` was not installed, so no ShellCheck result is claimed.
