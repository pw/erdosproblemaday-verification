# Erdős #864: exact 19-point boundary through N=135

This scratch bundle certifies the computational claim

```text
F(117) = ... = F(134) = 18, and F(135) = 19.
```

Here `F(N)` is the largest subset of `{1,...,N}` for which at most one
unordered pair-sum value has multiple representations (pairs `a <= b`, with
diagonal pairs allowed).

The proof has two independent exhaustive implementations:

- `search_direct.cpp` builds the exact reflected core one reflection orbit at
  a time, then adds all possible exact-core outliers.
- `audit_lowerhalf.cpp` instead enumerates Golomb lower halves, constructs
  cores in the reverse diameter order, counts sums directly, and uses a
  separate signed-coordinate bitset for outliers.

`REPORT.md` gives the completeness reduction, counts, controls, and the exact
finite-value inference.

## Fast checks

```bash
python3 verify_witness.py
python3 summarize_slices.py
python3 compare_counts.py
python3 replay_checks.py
sha256sum -c SHA256SUMS
```

## Rebuild and reproduce

```bash
g++ -O3 -DNDEBUG -std=c++17 search_direct.cpp -o search_direct
g++ -O3 -DNDEBUG -std=c++17 audit_lowerhalf.cpp -o audit_lowerhalf
./run_direct.sh
/usr/bin/time -v ./audit_lowerhalf
```

On the source VM, the captured independent `audit_lowerhalf` run used about
484 CPU seconds. The direct core-14 branch is split into 85 exact-center
slices and was run in parallel.

Exit status 2 from `search_direct` means that it found and printed a witness;
status 0 means that its requested branch was exhausted.
