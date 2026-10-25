# Hostile audit of the Erdős #813 order-18 computation

## Verdict

**PASS for publication as a computer-assisted result at solver-assertion
confidence.** No mathematical, encoding, census-coverage, case-coverage, or
persistent-assumption flaw was found. The result is not a globally
proof-certificate-verified UNSAT theorem: only four representative branches
have retained and replayed DRAT proofs.

The audited conclusion is `h(18)=5`:

- the explicit `W18` graph has clique number five and every seven-set contains
  a triangle;
- a hypothetical K5-free counterexample has maximum degree at least seven by
  the independently checked Brooks/color-class argument;
- the complete exact maximum-degree branches `d=7,8,9,10` were exhausted by
  CaDiCaL under signed census assumptions;
- the earlier `d=11,12` censuses were exhausted independently by CaDiCaL and
  Kissat; and
- the complete order-13 root-neighbourhood census is empty, excluding all
  larger degrees.

## Independent controls in this directory

`audit_censuses.py` uses only the Python standard library plus nauty's `geng`
and `shortg`. It regenerates every unlabeled graph of orders 7, 8, and 9,
filters from the definitions, and compares the exact H and M isomorphism
sets. It also independently refilters the audited order-10 parent census.

`audit_solver_logs.py` is stricter than the production log auditors. It
parses every result line, checks syntax, sequence number, shard congruence,
flat-index divmod, census sizes, graph edge counts, solver result, statistics,
terminal totals, absence of duplicates, and exact gap-free coverage. It also
audits the interrupted-plus-ten-reruns CaDiCaL degree-11 union directly rather
than trusting its consolidated TSV.

`audit_w18_upper.py` directly verifies symmetry, edge and triangle counts,
clique number five, and zero triangle-free seven-sets for the explicit upper
witness.

Run from this directory with the frozen result bundle as argument:

```bash
python3 audit_censuses.py /tmp/erdos813_h18_exact
python3 audit_solver_logs.py /tmp/erdos813_h18_exact
python3 audit_w18_upper.py
```

The stored logs are the exact output of these commands on 2026-08-12 UTC.

## Additional checks performed

- Every entry in the result bundle's SHA-256 manifest verified.
- The bundle's own `reproduce_audits.sh` completed with all checks passing.
- The exact CNF checker reconstructed all 43,656 natural clauses and
  exhaustively verified the existential projection of each sequential
  at-most-degree block over all `2^17` inputs for degrees 7 through 10.
- The four retained Kissat proofs (one each at degrees 7, 8, 9, and 10) were
  independently replayed with `drat-trim`; all returned `s VERIFIED`.
- The exact split logic was checked: after relabeling a maximum-degree root,
  global degree-at-most-`d` plus the 17 root units is exactly the branch
  `Delta=d`. Fixing all internal H/M edges and leaving all cross-edges free is
  exhaustive up to independent relabeling of the two parts.
- Reuse of one CaDiCaL instance is sound: assumptions are IPASIR decisions,
  and retained learned clauses are consequences of the shared base formula.

## Publication caveat

State explicitly that the millions of branch verdicts are solver assertions,
not individually retained proof certificates. Avoid `formally verified`,
`certificate complete`, or equivalent wording. `Computer-assisted; exhaustive
solver assertions with independently audited coverage` is accurate.
