# Exact dependency boundary

Site repository commit inspected for this extension:

```text
422d5f768c80dca1911d0c9fe8e3eb2197f10b62
```

The public base bundle is expected at
`verification/773/n69-frontier`.  Load-bearing base hashes are:

```text
7bc04a3ba3ee44ca07d298e5bfb1d363607f33fb06cfc9971435307a677fa2dd  SHA256SUMS
e5f029757634b869acd39bbdffd93278fe1f38375e4da9dbe36b8115cb4bf85a  README.md
eb21d0f429881f61dd5148ab2a41da3fb6b57d1513ea2db656ae3ae69883e933  dfs_hypergraph_coloring.cpp
dce8e0faa57f6373f1f9fa7e33afe1b1819723cf3a3535b1e4d94ad62d056916  oeis_A390813_b390813.txt
```

The exact upper theorem in this bundle assumes every row of
`prefix_bounds_through_70.txt` is a valid upper bound.  Rows 1 through 68 are
the byte-identical public OEIS prefix above; rows 69 and 70 are the conditional
exact results certified by that base bundle.  The complete extended file hash
is recorded in `SHA256SUMS`.

This dependency is logically sufficient because a hypothetical 34-set at 71
must contain 71 by `a(70)<=33`; after fixing 71, the exhaustive search asks
for exactly 33 lower indices.  At a recursive prefix `[k]`, replacing the
remaining constrained problem by the unconstrained maximum `a(k)` can only
weaken the upper bound, so every prefix prune is sound under the stated rows.

The lower witness and its 561 distinct integer sums do not depend on any
earlier computation.
