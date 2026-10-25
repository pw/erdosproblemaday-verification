# Exact MathDyad and site integration

Do not create another `erdos535_wave*.md`: the current ledger generator emits
every matching report and does not deduplicate problem numbers.  Refresh the
tracked file

```text
/home/exedev/MathDyad/runs/erdos535_wave9p.md
```

in place.  Change its date line to:

```text
Date: 2026-08-12 UTC (initial through-100 computation: 2026-07-28 UTC)
```

Replace its stale section 0 maintenance warning with the current live-gate
summary from this bundle's `LIVE_PROBLEM.txt` and `LIVE_DISCUSSION.txt`.  Add
the following immediately before the report's “What remains” section:

```markdown
## Exact extension from 101 through 125

**[d, computational-only]** Two complete independent enumerators now certify

\[
f_3(N)=
\begin{cases}
14,&101\le N\le107,\\
15,&108\le N\le124,\\
16,&N=125.
\end{cases}
\]

The lower witnesses lie at 101, 108, and 125.  Complete target-plus-one
searches return UNSAT at the right endpoints 107, 124, and 125, with 71,799,
109,838, and 113,132 forbidden gcd triples.  Monotonicity fills every value
in each interval.  A degree-ordered Python loop DFS and a separately written
natural-order C++ include/exclude search regenerate the hypergraph directly
and exhaust different trees.  A hostile third formulation checks the gcd /
prime-power-layer equivalence through 125 and exhausts every subset through
N=18.  The corrected lean bundle and audit are at
[`verification/535/f3-exact-through-125`](https://github.com/pw/ErdosProblemADay.com/tree/main/verification/535/f3-exact-through-125).

This is a finite exact extension only.  It gives no asymptotic improvement,
does not treat unrestricted r, and makes no historical novelty or priority
claim.
```

Replace the old terminal `PARTIAL:` line with exactly:

```text
PARTIAL: (d) Exact exhaustive certificates now give f_3(N) through N=125, with f_3(N)=14 for 101<=N<=107, 15 for 108<=N<=124, and 16 at N=125; the asymptotic problem remains open.
```

Commit the pre-existing through-100 verifier with the refreshed report:

```text
/home/exedev/MathDyad/runs/erdos535_wave9p_reverify.py
```

The first is pre-existing and currently untracked, but it is the base checker
explicitly named by the tracked through-100 report.  Commit it: otherwise the
published base reproduction command points to a missing file.  Keep the new
extension verifier in this public verification directory beside its frozen
live captures; the refreshed report links to this self-contained bundle.

Copy this lean bundle to:

```text
/home/exedev/ErdosProblemADay/verification/535/f3-exact-through-125/
```

Finally run:

```text
python3 /home/exedev/MathDyad/scripts/gen_erdos_ledger.py
```

and inspect the single generated row for problem 535.  Do not hand-edit
`src/ledger_data.js`.
