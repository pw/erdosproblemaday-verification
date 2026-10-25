# Integration-ready site text

Suggested artifact directory:

```text
verification/864/exact-through-135/
```

Suggested ledger summary:

> Exact finite extension **[D]**: a complete reflected-core enumeration,
> independently repeated by a Golomb-lower-half checker, proves that no valid
> 19-set has diameter at most 133. The normalized witness
> `{0,4,5,7,17,33,44,52,58,67,76,82,90,101,117,127,129,130,134}` has sole
> repeated sum 134 (ten representations). Hence
> `F(117)=...=F(134)=18` and `F(135)=19`.

Suggested report insertion after the existing 18-point result:

## Target 19: the next exact boundary

For a normalized 19-point set, the difference-reflection count leaves exactly
six possible exact reflected-core sizes under diameter 133:

| core size | outliers | distinct-difference lower bound |
|---:|---:|---:|
| 19 | 0 | 90 |
| 18 | 1 | 99 |
| 17 | 2 | 107 |
| 16 | 3 | 115 |
| 15 | 4 | 122 |
| 14 | 5 | 129 |

A 13-point core would already force diameter at least
`171-(7-1)^2=135`, and smaller cores are no better. Thus the classification
is complete. **[A]**

Two independently organized exhaustive implementations then exclude all six
cases through diameter 133. The direct reflected-orbit search and the
Golomb-lower-half audit agree on every valid-core count:

```text
core 19:          0
core 18:      1,297
core 17:     22,271
core 16:  1,920,748
core 15:  1,565,022
core 14: 22,183,488
```

No core extends to 19 points. **[D]**

The normalized witness

```text
{0,4,5,7,17,33,44,52,58,67,76,82,90,101,117,127,129,130,134}
```

has only the repeated sum

```text
134 = 0+134 = 4+130 = 5+129 = 7+127 = 17+117
    = 33+101 = 44+90 = 52+82 = 58+76 = 67+67.
```

Translating by one gives a valid 19-set in `[135]`. Together with the
previously certified 18-point witness of diameter 116, the nonexistence result
gives

```text
F(117)=F(118)=...=F(134)=18.
```

Finally `F(N+1) <= F(N)+1`, since deleting `N+1` from a set loses at most one
point. The new witness therefore also proves

```text
F(135)=19.
```

The full reduction, sources, frozen outputs, independent audit, sanitizer and
debug controls, exact-center coverage check, and SHA-256 manifest are in the
verification bundle. **[D]**

## Files worth publishing

- `README.md`
- `REPORT.md`
- `search_direct.cpp`
- `audit_lowerhalf.cpp`
- `run_direct.sh`
- `verify_witness.py`
- `summarize_slices.py`
- `compare_counts.py`
- `replay_checks.py`
- all `direct_core*.log`
- `audit_output.txt`, `audit_time.txt`
- `control18_core*.log`
- `sanitizer_output.txt`, `debug_positive_output.txt`
- `live_gate.txt`
- `witness_output.txt`, `slice_summary.txt`, `count_comparison.txt`,
  `replay_output.txt`
- `SHA256SUMS`
