# Scratch-only site update draft for Problem 1109

This is publication copy for the existing `1109-squarefree-sumset` entry. It
does not replace or retract the 24 July analytic attempt; the new section
should be inserted at the start of that entry's body.

## Suggested title

`#1109: exact squarefree-sumset frontier through 1500`

## Suggested summary

```js
"The asymptotic problem remains open. A new exact computation extends " +
"OEIS A392165 by five record indices: 1255, 1277, 1293, 1335, and 1407, " +
"and proves f(N) exactly through N=1500. A custom verifier, Cliquer, and " +
"PMC agree on every eligible last-vertex decision. This is a finite update " +
"to the site's 24 July attempt, not an asymptotic improvement."
```

## HTML body fragment

```html
<p><strong>Exact finite update (11 August).</strong> Let f(N) be the largest
size of A &subseteq; {1,...,N} for which every sum in A+A, including each
diagonal sum 2a, is squarefree. The next five record indices after the
published frontier at 1103 are</p>

<p style="text-align:center"><strong>
f(1255)=40, &nbsp; f(1277)=41, &nbsp; f(1293)=42,<br>
f(1335)=43, &nbsp; and &nbsp; f(1407)=44.
</strong></p>

<p>Equivalently, f(N)=39 on 1103&le;N&le;1254, then equals 40, 41, 42,
and 43 on 1255&ndash;1276, 1277&ndash;1292, 1293&ndash;1334, and
1335&ndash;1406 respectively, and f(N)=44 throughout 1407&le;N&le;1500.
These are the next five terms of OEIS A392165 as it stood on 11 August
2026.</p>

<p><strong>Why the computation is exact.</strong> Use a graph whose vertices
are the a&le;N with 2a squarefree and whose edges join distinct a,b when
a+b is squarefree. Then f(N) is exactly its clique number. When a new
eligible vertex N is added, the optimum rises from r to r+1 exactly when
its old-neighbor graph contains an r-clique. Checking that decision for
every eligible N proves every prefix by induction; ineligible N leave the
graph unchanged.</p>

<p>The primary C++ verifier uses an exhaustive independent-set coloring
bound and reproduces all 39 previously published transitions before finding
the five above. A direct checker verifies all five displayed lower
certificates sum by sum. Two external exact solvers then independently
check all 163 eligible last-vertex graphs from 1104 through 1500: Ubuntu
Cliquer 1.21 from DIMACS graphs and official PMC from Matrix Market graphs.
They agree with the primary verifier on every decision and find no further
jump through 1500. The frozen verification bundle includes sources,
solver provenance, logs, graph digests, witnesses, sanitizer output, and a
cold cross-audit.</p>

<p><strong>Scope.</strong> This is an exact finite extension only. It does not
improve Konyagin's asymptotic upper bound and does not resolve Erdos's
N<sup>o(1)</sup>, or possible polylogarithmic, conjecture. The site already
treated Problem 1109 on 24 July; that analytic attempt remains below. This
section records a later finite result, not the site's first attempt and not
a solution of the parent problem.</p>
```

## Suggested link

```js
{
  label: "Exact frontier through 1500: report, source, logs, and audits",
  url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1109"
}
```
