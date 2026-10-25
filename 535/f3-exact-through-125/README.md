# Erdős #535: exact `f_3(N)` values through 125

Frozen 2026-08-12 UTC.  This dependency-free finite exact bundle extends the
site's previously checked table through 100 by proving

```text
f_3(N) = 14  for 101 <= N <= 107,
f_3(N) = 15  for 108 <= N <= 124,
f_3(125) = 16.
```

It does not improve the asymptotic bounds, treat unrestricted `r`, solve
Problem 535, or claim historical novelty or priority.

## Reproduce from a clean copy

```sh
./reproduce.sh
```

The Python and C++ programs independently generate the complete gcd
hypergraph and exhaust target-plus-one searches at the three right endpoints.
The C++ executable is generated outside this bundle so reproduction cannot
change a manifest-pinned file.

`REPORT.md` gives the proof, search-completeness argument, witnesses, edge and
node counts, timing, live collision gate, and exact scope.  `HOSTILE_AUDIT.md`
records the independent audit and final PUBLISH verdict;
`hostile_audit_535.py` supplies its third, small-universe formulation.

This lean payload intentionally contains no compiled executable,
`__pycache__`, `.pyc`, or empty compiler logs.  The retained sanitizer output
and timing record document a completed ASan+UBSan replay; they are not needed
for the primary proof.  `verify_535_extension.log` and
`independent_verify.log` are the canonical deterministic stdout records to
which clean replays are compared byte-for-byte.

## Integration targets

- Public verification path:
  `ErdosProblemADay/verification/535/f3-exact-through-125/`.
- Replace the existing MathDyad report at
  `MathDyad/runs/erdos535_wave9p.md` with a refreshed combined report dated
  2026-08-12; do not create a second `erdos535_wave*.md`, because the ledger
  generator emits one row per matching report rather than deduplicating by
  problem number.
- Commit the existing base checker
  `MathDyad/runs/erdos535_wave9p_reverify.py` together with that report.  It is
  currently untracked but is the verifier explicitly named by, and embedded
  in, the tracked through-100 report.  Keeping it makes the base table
  reproducible.
- Keep the new primary verifier in this public verification directory, beside
  its manifest-pinned live captures.  The refreshed MathDyad report points
  here; copying the verifier alone would break its capture-relative live-gate
  checks.
- Regenerate `ErdosProblemADay/src/ledger_data.js` with
  `MathDyad/scripts/gen_erdos_ledger.py`; do not edit generated ledger data by
  hand.

`MATHDYAD_INTEGRATION.md` gives the exact insertion text and replacement
verdict line.

Suggested final MathDyad verdict line:

```text
PARTIAL: (d) Exact exhaustive certificates now give f_3(N) through N=125, with f_3(N)=14 for 101<=N<=107, 15 for 108<=N<=124, and 16 at N=125; the asymptotic problem remains open.
```

Suggested ledger gist:

```text
Exact exhaustive certificates extend the r=3 table through 125: f_3=14 on 101..107, 15 on 108..124, and 16 at 125; Problem 535 remains asymptotically open.
```
