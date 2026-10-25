# Sources and claim boundary

This package proves a finite `n=4` theorem. It does not settle the asymptotic
question on the official Problem 1131 page.

Sources checked while preparing the package:

* Official statement and status: <https://www.erdosproblems.com/1131>
* Official comment thread, checked in both orders:
  <https://www.erdosproblems.com/forum/thread/1131?order=oldest> and
  <https://www.erdosproblems.com/forum/thread/1131?order=newest>
* P. Erdos, J. Szabados, A. K. Varma, and P. Vertesi (1994), full primary
  volume scan: <https://real-j.mtak.hu/5471/1/StudScientMath_29.pdf>
* L. Brutman and D. Toledano (1997), DOI record and abstract:
  <https://doi.org/10.1016/S0898-1221(97)00232-0>, ScienceDirect PII
  `S0898122197002320`
* R. Zeraoulia (2026), non-peer-reviewed preprint, inspected only to test a
  displayed formula: <https://www.preprints.org/manuscript/202601.0875/v1>

Brutman-Toledano (1997) numerically computed high-precision minima for
`n=3,...,100`, so the four-node optimizer and minimum were already known
numerically. Its abstract describes numerical optimization, Richardson
extrapolation, asymptotics, and heuristic near-optimal nodes. Elsevier metadata
labels the article as an open-archive article, but the complete article and its
prior references have not yet been checked for an exact small-`n` theorem. The
present contribution is an independently checkable exact global certificate
and algebraic characterization. This package makes no novelty or priority
claim for the theorem, proof, nodes, decimal, exact formulas, or algebraic
value.

As checked on 2026-08-11, the official page was open and had no formal proof
record or current-worker tag. Its five comments already included a 1997
literature pointer, an asymptotic claimed disproof posted on 2026-04-26, and a
standard-check reply posted on 2026-04-27. Thus this package does not describe
the live record as having zero claimed proofs. None of those comments states
the exact finite `n=4` certificate given here.

Exact web searches for the critical cubic and minimum-polynomial coefficient
strings found no mathematical source. That search miss is not evidence of
novelty and does not replace the outstanding full-source review.

The 2026 preprint is not used as verification. Its displayed identity
`I_n=2-2/n` for the Legendre-integral nodes fails at `n=4`: exact integration
gives `12/7`, rather than `3/2`. The classical value is `2-2/(2n-1)`.

No third-party paper or PDF is redistributed in this bundle.
