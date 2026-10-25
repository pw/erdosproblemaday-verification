# Integration notes

Suggested public location:

```text
verification/840/s-k-n-exact-through-32/
```

Suggested conservative ledger outcome:

```text
The exact finite proxy is extended from n<=27 through n=32. The prior checker
included in this bundle certifies all rows through n=27; a new complete
2^31-subset traversal supplies rows n=28,...,32. The six nontrivial n=32 upper
cells also have independently replayed SAT/DRAT certificates. This is finite
computational progress only; Problem #840 remains open.
```

Suggested MathDyad report addition:

```markdown
## 2026-08-12 exact extension through 32

The finite Pikhurko proxy is now certified through `n=32`.  In particular,
\[
(s(k,32))_{k=1}^{32}=
(1,3,6,10,15,21,28,35,42,51,55,59,62,63,\ldots,63).
\]
The producer enumerated exactly `2^31` translated subsets.  The six
nontrivial upper cells `k=8,...,13` were regenerated directly as SAT instances;
CaDiCaL and Kissat both returned UNSAT and every CaDiCaL proof replayed under
`drat-trim`.  This is an exact finite extension, not an asymptotic improvement,
and Problem #840 remains open.
```

Integration order:

1. Run `python3 verify_bundle.py` (fast full producer replay).
2. Run `python3 verify_bundle.py --quick --replay-drat` with the bundled or
   system `drat-trim`; this is the slower proof-certificate gate.
3. Copy the closed bundle to the site verification path.
4. Append the conservative update to `runs/erdos840_wavew018.md`; keep the old
   `n<=27` Python verifier as the independent historical baseline.
5. Regenerate the site ledger, commit only the targeted #840 files, deploy,
   purge, and verify the canonical report URL.

Do not integrate the separate provisional `n<=37` producer output into this
checkpoint.  It has direct exhaustive evidence but has not received the six-
cell terminal SAT/DRAT audit used here.
