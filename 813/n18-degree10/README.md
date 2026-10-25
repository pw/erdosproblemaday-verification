# Problem 813: order-18 degree reduction

This bundle supports the 12 August 2026 computational reduction for the
finite boundary in Erdős problem 813:

> Any 18-vertex `K5`-free graph in which every seven vertices contain a
> triangle must have maximum degree at most 10.

The exact value remains open: the bundle neither constructs such a graph nor
proves that none exists. The final 411 UNSAT outcomes are matching CaDiCaL
1.9.5 and Kissat 4.0.4 results, not DRAT/LRAT proof certificates.

The complementary rigorous reduction, modulo Brooks' theorem, is that every
candidate has maximum degree at least 7. Its full proof is `DELTA7_PROOF.md`
and its dependency-free finite audit is `delta7_check.py`. Thus the current
candidate window is `7 <= Delta <= 10`, with the upper endpoint retaining the
solver caveat above.

## Fast checks

From this directory:

```bash
sha256sum -c SHA256SUMS
python3 delta7_check.py
python3 verify_near.py
python3 hostile_audit/audit_813.py
```

The hostile audit checks the graph6 files from their bytes, the census
cardinalities and defining properties, the exact coverage of both solver log
families, the natural CNF dimensions, and the nine-defect graph. Its full run
uses `nauty-shortg`, NetworkX, and PySAT; the audit logic itself is independent
of the producer's census implementation.

## Full census check

With NetworkX and `nauty-shortg` installed:

```bash
python3 -u census_verify.py \
  census_n10.g6 census_n11.g6 census_n12.g6 census_n13.g6
```

This independently regenerates every valid extension from orders 10 through
13 and demands byte-for-byte equality after canonicalisation. It takes about
a minute on the publication host.

## Re-running SAT cases

With PySAT and the relevant backend installed, the generic driver handles
both degrees. For example:

```bash
python3 -u neighbourhood_census_sat.py \
  11 census_n11.g6 0 8 --solver cadical195
python3 -u neighbourhood_census_sat.py \
  12 census_n12.g6 0 1 --solver kissat404
```

Run every shard to reproduce a full solver family. A satisfying result is
decoded and independently checked before it is printed. `near_sat.py` is a
separate bounded Hamming-ball diagnostic around `best9.masks`.

`REPORT.md` contains the mathematical argument, exact counts, timings, and
the distinction between the audited census and uncertified solver verdicts.
