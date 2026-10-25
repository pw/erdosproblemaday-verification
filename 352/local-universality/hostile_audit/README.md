# Frozen hostile-audit scope

Verdict: **BLOCK the source bundle's current ambiguous coloring wording;
PUBLISH after the normalization-scope correction in `AUDIT_REPORT.md`.**

The all-`N` geometric lemma, the full progression clique, and the coloring
obstruction for one map common to every oriented/unnormalized branch are
rigorous.  No simple D4 symmetrization retains `O(N)` colors.  A conclusion
about one map common only to normalized branch representatives is not proved.

Run the independent checker with assertions enabled:

```text
python3 independent_audit.py
```

Files:

- `AUDIT_REPORT.md`: complete proof audit, exact correction, and D4 analysis;
- `independent_audit.py`: independent exact construction and full-triple
  checker;
- `INDEPENDENT_OUTPUT.txt`: frozen output;
- `SOURCE_SHA256SUMS`: identity of the audited source bundle and cold replay;
- `SHA256SUMS`: hashes of the hostile-audit artifacts.
