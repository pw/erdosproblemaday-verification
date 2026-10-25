# Problem 168 finite frontier through 5,020

This directory preserves two immutable evidence bundles:

- `author/`: the original computation and solver-free witness checks;
- `hostile_audit/`: an independent reconstruction and reversed-formulation
  SCIP rerun, plus unsuccessful CBC and SAT falsification attempts.

The supported result is a conventional floating-MIP computation:
`f(5000)=3335` through `f(5020)=3347`, adding twelve first-hit rows to
OEIS A004059. It is not a proof-carrying exact certificate, and it does not
settle the density or irrationality questions in Problem 168.

Run `./reproduce.sh` for the portable, solver-free integrity and witness audit.
The original SCIP transcripts and independent rerun logs are frozen in the two
bundles.
