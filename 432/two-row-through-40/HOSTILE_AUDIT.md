# Hostile audit verdict

Verdict: **PUBLISH**, as computational-only finite progress.

An independent audit rederived the sum-preserving normalization for arbitrary
positive rows and columns, checked that every lower-bound gap is searched,
and verified that witness existence at `L_n`, nonexistence at `L_n-1`, and
monotonicity prove each exact threshold.

Both bundled engines were rebuilt and rerun from scratch. Every non-timing
line of the 30-row C++ gcd-clique and CP-SAT prime-support transcripts was
reproduced. A separate parser reconstructed normalized rows and columns and
checked all cardinalities, distinct sums, pairwise gcds, and exact maximum
sum. The `n=40` AddressSanitizer/UndefinedBehaviorSanitizer run also passed.

A third formulation audited the hardest lower endpoint `x=508` using direct
gcd-conflict CNFs and an independently generated sequential `>=40` encoding.
Odd gaps are impossible by parity; 51 even gaps have fewer than 40 candidates;
all remaining 202 even-gap formulas were UNSAT in CaDiCaL. In aggregate this
checked 697,700 variables and 2,330,472 clauses in 49.37 seconds.

The audit independently refetched the live problem and discussion pages on
2026-08-12: status OPEN, zero claimed proofs, no current worker, and one
partial-results comment. Sungchul Lee's public June manuscript already uses
the coprime-grid terminology and CRT finite-grid extension. Accordingly, the
report credits that framework and claims only the exact finite threshold
extension computed in this project.
