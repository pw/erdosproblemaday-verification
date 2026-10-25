# Erdős Problem 535: exact finite extension through 125

Date: 2026-08-12 UTC.

## Result

For \(r=3\), let \(f_3(N)\) be the largest size of a set
\(A\subseteq\{1,\ldots,N\}\) containing no three distinct elements whose
three pairwise greatest common divisors are equal.  Two complete, independent
enumerators certify

\[
f_3(N)=
\begin{cases}
14,&101\le N\le107,\\
15,&108\le N\le124,\\
16,&N=125.
\end{cases}
\]

Thus the first two transition indices after the previously checked table
through 100 are 108 and 125.  This is an exact computer-assisted finite
extension.  It does not improve the asymptotic bounds, treat arbitrary \(r\),
or solve Problem 535.  No historical novelty or priority is claimed.

## Live collision gate

`LIVE_PROBLEM.txt` and `LIVE_DISCUSSION.txt` are complete rendered Bright Data
captures made before the computation.  At access time the page was:

- `OPEN`;
- at `0 claimed proofs for this problem`;
- with no interested collaborator, current worker, or current formalizer;
- accompanied by nine comments.

The complete thread discusses asymptotic sunflower bounds, a correction from
\(\omega\) to \(\Omega\) in an auxiliary formulation, and citations.  It does
not state a finite table or certificate.

The separate records check is in `RECORDS_GATE.md`.  In particular, the live
page labels the OEIS field only `Possible`; it names no sequence.  The existing
ErdosProblemADay exact table ends at 100.  Targeted exact-wording and value
searches found no competing table, but this is only a source-surface search
result, not a novelty theorem.

## Exact reduction

Construct the 3-uniform hypergraph \(H_N\) on vertices \(1,\ldots,N\), with

\[
\{a,b,c\}\in E(H_N)
\quad\Longleftrightarrow\quad
\gcd(a,b)=\gcd(a,c)=\gcd(b,c).
\]

The forbidden sets in the definition are exactly the hyperedges, so
\(f_3(N)=\alpha(H_N)\).  Both verifiers generate every hyperedge directly from
this gcd equality; no factor table, SAT output, or previous finite table is an
input.

## Lower certificates

The following independent sets occur at the left endpoints:

```text
N=101, size 14:
10,12,13,15,18,20,24,40,48,54,75,80,91,96

N=108, size 15:
11,14,20,24,30,33,36,40,48,80,90,96,98,99,108

N=125, size 16:
14,20,21,24,25,30,36,40,48,63,80,90,96,98,108,125
```

Each verifier checks all triples in each displayed set directly.

## Upper certificates and interval logic

Complete searches return UNSAT for:

| endpoint | forbidden target size | hyperedges | Python DFS nodes | independent C++ binary nodes |
|---:|---:|---:|---:|---:|
| 107 | 15 | 71,799 | 4,225,121 | 11,898,873 |
| 124 | 16 | 109,838 | 11,638,943 | 37,336,183 |
| 125 | 17 | 113,132 | 8,579,402 | 32,227,421 |

A lower witness at the left endpoint and an upper certificate at the right
endpoint prove the whole row by monotonicity of \(f_3(N)\).  Notice that the
extension is self-contained: although its interpretation continues the public
through-100 table, none of its three interval proofs assumes an old optimum.

## Why the searches are complete

The Python verifier fixes a degree-descending vertex order.  A state contains
an independent chosen set and the bit mask of later candidates.  Choosing a
candidate \(v\) removes exactly those candidates \(w\) for which some already
chosen \(u\) completes the hyperedge \(\{u,v,w\}\).  Each subset therefore has
one unique increasing representation.  The search prunes only a completed
forbidden triple or an insufficient number of remaining candidates.  Exhausting
the tree without reaching the target proves UNSAT.

The independent C++ verifier does not read Python output.  It uses increasing
integer order rather than hypergraph-degree order and a binary include/exclude
recursion rather than the Python loop recursion.  It independently generates
the gcd hypergraph, checks all three lower witnesses, and exhausts visibly
different search trees.  The exact edge counts agree.

## Frozen runs

The dependency-free Python run completed in 32.23 seconds, used 26,196 KiB
maximum resident memory, and exited 0.  The independent C++ run completed in
1.66 seconds, used 6,348 KiB, and exited 0.  Both were run single-threaded at
Unix niceness 15.  The C++ verifier was also rebuilt with AddressSanitizer and
UndefinedBehaviorSanitizer and repeated all three endpoint searches with no
diagnostic. Deterministic expected stdout and GNU-time records are included;
empty compiler logs were intentionally omitted from the lean public bundle.

The compact 25-value table has SHA-256

```text
c4663eebc814f6a00fd78b590cea0aab34e5542f822759ddd339ddf0733df968
```

when encoded as compact JSON.

## Reproduction

```sh
python3 verify_535_extension.py | tee /tmp/verify535.python.log
cmp /tmp/verify535.python.log verify_535_extension.log

g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic \
  independent_verify.cpp -o /tmp/verify535
/tmp/verify535 | tee /tmp/verify535.cpp.log
cmp /tmp/verify535.cpp.log independent_verify.log

python3 hostile_audit_535.py | tee /tmp/verify535.audit.log
cmp /tmp/verify535.audit.log hostile_audit_535.log

sha256sum -c SHA256SUMS
```

`SHA256SUMS` covers every frozen source, capture, report, and log except the
manifest itself.  Generated binaries and Python bytecode are deliberately not
part of the public bundle.
