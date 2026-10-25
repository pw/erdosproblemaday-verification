# Erdős #425: exact strict-pair values through 61

Frozen 2026-08-12 UTC.  This self-contained, standard-library primary bundle
extends the previously certified frontier `F(50)=26` to

```text
n : 50 51 52 53 54 55 56 57 58 59 60 61
F : 26 26 27 28 28 28 29 29 29 30 30 31
```

Here `F(n)` is the maximum size of `A subset [n]` for which the products
`ab` are distinct over all strict pairs `a<b` in `A`.  This is finite exact
progress only; neither asymptotic question in Problem 425 is solved.

## Live gate

`LIVE_GATE.txt` is a Bright Data browser transcript from 2026-08-12.  It
records `OPEN`, `0 claimed proofs for this problem`, and
`Currently working on this problem: None`.  Thus the collision gate passed.

## Reproduce

Primary exact search, using only Python's standard library:

```bash
python3 base_erdos425_wave9i_verify.py
python3 verify_425_through_61.py
```

The first command replays the prior exact table through 50.  The second
independently builds the obstruction hypergraph in two ways, checks the five
new jump witnesses at definition level, and performs exhaustive
branch-and-bound upper searches at plateau endpoints.  The two commands took
about eight minutes in the loaded hostile-audit run.  The extension also
checks the exact SHA-256 of the frozen base snapshot, so it resolves no
external repository path.

Fast hostile controls:

```bash
python3 audit_425_witnesses.py
python3 audit_425_logic.py
```

The first rebuilds all strict-pair products directly.  The second exhausts
4,096 counter truth-table cases, agrees on obstruction generation through
`n=20`, and checks full SAT/direct-definition equivalence through `n=9`.

Independent SAT rerun (external CaDiCaL, Kissat, and `drat-trim` required):

```bash
CADICAL=/path/to/cadical \
KISSAT=/path/to/kissat \
DRAT_TRIM=/path/to/drat-trim \
python3 audit_425_sat.py
```

It generates every obstruction directly from four-subsets, encodes the
deletion bound with a Sinz sequential counter, asks both solvers to reject
the five plateau violations, and replays CaDiCaL's DRAT output. The full set
of generated CNFs and untrimmed DRAT proofs is deliberately not
retained: it totals hundreds of megabytes and is deterministically
regenerable.  The compact bundle retains the exact scripts, solver logs,
CNF/proof hashes, and all five replay summaries.  It also retains one complete
compressed replayable regression certificate at `n=50`:

```bash
cd replay_control_n50
gzip -dk upper_n50_F26.drat.gz
/path/to/drat-trim upper_n50_F26.cnf upper_n50_F26.drat
```

Accordingly the extension claim is labelled **computational-only** and rests
primarily on the retained standard-library exhaustive search; the two solver
runs and five successful proof replays are independent hostile controls, not
a full set of permanently shipped certificates for the new endpoints.

## Why the plateau proof is complete

Always `F(n-1) <= F(n) <= F(n-1)+1`.  The jump witnesses therefore prove the
exact values at the jump points 52, 53, 56, 59, and 61.  For a constant plateau
`[lo,hi]` of value `k`, a witness at `lo` gives every lower bound while an
exhaustive rejection of a vertex cover of size `hi-k-1` in the obstruction
hypergraph gives `F(hi)<=k`; monotonicity fills the interval.  Upper searches
are run at 51, 55, 58, and 60, with the old endpoint 50 independently rerun
as a regression control.

## Integration targets

- Append the finite table/result and method to
  `MathDyad/runs/erdos425_wave9i.md`, redating the refreshed report.
- Add this lean directory at
  `ErdosProblemADay/verification/425/exact-through-61/`.
- Regenerate the site ledger from the refreshed MathDyad report.
- Suggested gist: “Exact strict-pair values are certified through 61:
  F(51..61)=26,27,28,28,28,29,29,29,30,30,31; the asymptotic constant and
  higher-r problem remain open.”
