# Independent finite extension report: Erdős #425 through 61

Date: 2026-08-12 UTC.

## Exact theorem (computational-only)

Let `F(n)` denote the maximum cardinality of `A subseteq {1,...,n}` such that
all products `ab`, over unordered pairs of distinct elements `a,b in A`, are
distinct.  Exact exhaustive computation gives

```text
F(51)=26, F(52)=27, F(53)=28, F(54)=28, F(55)=28,
F(56)=29, F(57)=29, F(58)=29, F(59)=30, F(60)=30, F(61)=31.
```

Together with the prior `F(50)=26`, this is the full exact table through 61.
It does not imply either asymptotic assertion in Erdős Problem 425.

## Verification layers

1. The retained standard-library checker independently generates every
   multiplicative-collision four-edge both by equal-product pairs and by all
   four-subsets; at `n=61` both give exactly 1,173 edges.
2. Exact branch-and-bound rejects all one-too-small covers at plateau right
   endpoints 50, 51, 55, 58, and 60.  It reports respectively 120,900;
   254,913; 428,011; 748,428; and 1,036,845 recursive nodes.
3. Five explicit new witnesses are checked directly, with respectively 351,
   378, 406, 435, and 465 distinct strict-pair products.
4. A separately written SAT generator uses four-subset edge enumeration and
   a Sinz sequential counter.  CaDiCaL and Kissat independently returned
   UNSAT for every plateau endpoint.  All five CaDiCaL DRAT proofs were
   successfully replayed by `drat-trim`; compact logs record the runs.  The
   complete `n=50` replay control is retained compressed, while large new-
   endpoint proofs are not distributed, so those are audited solver controls
   rather than portable retained certificates.
5. The counter encoding was exhaustively compared with its truth table in
   4,096 cases; the complete CNF was compared with direct subset enumeration
   through `n=9` in 54 decision cases.

Confidence is high for a finite computational result.  Label `[d]`; do not
describe it as a solution of Problem 425 or as proof-certified independently
of execution.
