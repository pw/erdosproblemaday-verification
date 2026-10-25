# Erdős problem 813: the order-18 boundary, 2026-08-12

## Live gate

Bright Data fetched <https://www.erdosproblems.com/813> on 2026-08-12 UTC.
The page was `OPEN`, with 0 comments, 0 claimed proofs, and nobody listed as
currently working or interested in collaborating.

Write

\[
\alpha_3(G)=\max\{|S|:G[S]\text{ is triangle-free}\}.
\]

The unresolved finite question from the previous report is whether there is
an 18-vertex graph satisfying

\[
\omega(G)\leq4,\qquad \alpha_3(G)\leq6.                 \tag{1}
\]

Such a graph would prove \(h(18)=4\); nonexistence would prove \(h(18)=5\).
This run did **not** settle that question.  It gives a substantial exact
reduction and a much closer explicit near miss.

## Main new reduction

The computational conclusion, independently reproduced by CaDiCaL 1.9.5
and Kissat 4.0.4, is:

> If a graph satisfying (1) exists, its maximum degree is at most 10.

The prior report proved only \(\Delta(G)\leq12\).

### The neighbourhood census

Let \(\mathcal C_d\) be the isomorphism classes of \(d\)-vertex graphs \(H\)
which are \(K_4\)-free and have \(\alpha_3(H)\leq6\).  A complete hereditary
census gives

| \(d\) | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| \(|\mathcal C_d|\) | 578 | 3,128 | 11,005 | 9,133 | 403 | 8 | 0 |

The key elementary augmentation criterion is as follows.  Suppose
\(H\in\mathcal C_d\), and add a new vertex with neighbourhood \(A\subseteq
V(H)\).  The child is in \(\mathcal C_{d+1}\) exactly when

1. \(A\) is triangle-free, so no new \(K_4\) is created; and
2. for every triangle-free six-set \(S\) in \(H\), the intersection
   \(A\cap S\) contains an edge, so \(S\) together with the new vertex is
   not triangle-free.

In particular \(|A|\leq6\).  This enumerates every child because both
properties defining \(\mathcal C_d\) are induced-hereditary.

The existing C producer generated 3,989 valid labelled extensions from the
9,133 order-10 parents, which canonicalised to 403 order-11 types; then 16
labelled extensions canonicalised to 8 order-12 types; the 8 order-12 types
have no valid extension.  A new, independent Python verifier rebuilt every
extension directly from the two defining conditions and obtained exactly
the same canonical files byte-for-byte:

```text
TRANSITION 9133->403: valid_labelled_extensions=3989 canonical_byte_comparison=PASS COMPLETE
TRANSITION 403->8: valid_labelled_extensions=16 canonical_byte_comparison=PASS COMPLETE
TRANSITION 8->0: valid_labelled_extensions=0 canonical_byte_comparison=PASS COMPLETE
```

As an augmentation-independent control at order 10, `nauty-geng` generated
all 12,005,168 unlabeled ten-vertex graphs.  Direct definition filtering
left 9,133 graphs, and canonicalising them produced exactly the same bytes
and SHA-256 as the augmentation census:

```text
234be06b2b8dbadec010e95ec0f62fffbe936a21207654f521742c063321ff0c  census_n10.g6
234be06b2b8dbadec010e95ec0f62fffbe936a21207654f521742c063321ff0c  direct_n10_canon.g6
```

The remaining census hashes are:

```text
5c519de3308a947bbdfbda8db4ad02b4f6e9435247204c571730b931a9069e50  census_n11.g6
178c371f2e88e09bfd3462f225496c5e8910eb2e779a6cfcd7ecb001c07e4b0c  census_n12.g6
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  census_n13.g6
```

### Exhausting degree 12 and degree 11

If \(G\) satisfies (1), then \(G[N(v)]\) is \(K_4\)-free: a \(K_4\) there,
together with \(v\), would be a \(K_5\).  It also has
\(\alpha_3(G[N(v)])\leq6\), because every seven vertices of \(G\), hence
every seven vertices in the neighbourhood, contain a triangle.  Thus a
degree-\(d\) neighbourhood belongs to \(\mathcal C_d\).

For each of the 8 order-12 and 403 order-11 census representatives, the
checker rebuilt the natural 18-vertex CNF from the definition:

- 153 edge variables and 816 triangle variables;
- four clauses for
  \(t_{ijk}\leftrightarrow(e_{ij}\wedge e_{ik}\wedge e_{jk})\);
- one missing-edge clause for every five-set, forbidding \(K_5\);
- one triangle clause for every seven-set;
- 17 units fixing \(N(0)=\{1,\ldots,d\}\);
- \(\binom d2\) units fixing the induced neighbourhood representative.

No maximum-degree assumption is inserted.  Hence the cases exhaust every
graph having even one vertex of degree \(d\).

CaDiCaL returned UNSAT in all 411 cases.  For degree 11 the 403 cases used
34,864,416 conflicts and 2,307.669 aggregate solver-seconds; the slowest
case took 38.498 seconds.  For degree 12 the 8 cases used 118,752 conflicts
and about 4.3 aggregate solver-seconds.  Kissat independently returned
UNSAT on the same 411 definition-generated formulas.  Its degree-11 run
used 1,621.060 aggregate solver-seconds, with a slowest case of 26.420
seconds; PySAT's Kissat backend does not expose conflict counts.

Since \(\mathcal C_{13}\) is empty, degree at least 13 is impossible as
well: any 13 neighbours would induce a member of \(\mathcal C_{13}\).
The degree-11 and degree-12 exhaustions therefore prove the stated reduction
\(\Delta(G)\leq10\), modulo the finite solver results.

### Certificate status

This distinction matters.  The census is reproducible and audited at the
definition level, with an independent extension implementation and direct
order-10 enumeration.  The final 411 UNSAT verdicts are two-solver
assertions, **not** DRAT/LRAT-certified proofs.  They are high-confidence
finite results, but not independently replayable proof certificates.

## A close near miss

Local search found the following 18-vertex graph, given by hexadecimal
adjacency masks:

```text
2575c 3c53c 30fe3 1df83 3ee43 3e1c6
17b35 37e2c 0bc6f 298dd 2699f 1a7dc
2e3c9 2ddf0 134fb 33b3a 0c8fe 0b6b7
```

A dependency-free checker gives:

```text
n                      : 18
edges                  : 96
triangles              : 180
K5 count               : 0
triangle-free 7-sets   : 9
omega (exact)          : 4
VALID h(18)=4 WITNESS  : False
```

Its degree sequence is \(10^6 11^{12}\), and its automorphism group has
order 12.  The nine bad seven-sets fall into three overlapping clusters.
Every single-edge addition which repairs any of them creates at least three
\(K_5\)'s.  Exact Hamming-ball SAT runs found no true witness within seven
edge flips of this graph.  This is search information, not a lower bound on
all witnesses.

Guided local search, including dynamically weighted bad-seven-set and
\(K_5\) penalties, did not improve below nine bad seven-sets while remaining
\(K_5\)-free.  Searches allowed to violate both constraint families reached
five total violations, but not zero.

## Reproduction artifacts

All new work is frozen under `/tmp/erdos813_attack/`:

- `census_n10.g6`, `census_n11.g6`, `census_n12.g6`, `census_n13.g6`;
- `direct_n10.g6` and `direct_n10_canon.g6`;
- `census_verify.py` and `census_verify.log`;
- `d12_census_sat.py`, `neighbourhood_census_sat.py`;
- `d11_all_cases.tsv`, the CaDiCaL per-case record;
- `d11_kissat_all_cases.tsv`, the consolidated Kissat per-case record;
- `d11_kissat_shard*.log`, the independent Kissat records;
- `best9.masks`, `near_sat.py`, `tabu_both.c`;
- `MANIFEST.sha256`.

The central commands are:

```bash
python3 -u census_verify.py \
  census_n10.g6 census_n11.g6 census_n12.g6 census_n13.g6

python3 -u neighbourhood_census_sat.py \
  11 census_n11.g6 SHARD SHARDS --solver cadical195

python3 -u neighbourhood_census_sat.py \
  11 census_n11.g6 SHARD SHARDS --solver kissat404
```

`census_verify.py` requires NetworkX and the `nauty-shortg` executable;
the SAT checker requires PySAT with the named solver backends.

PARTIAL: reduced the residual h(18)=4 witness question to maximum degree at
most 10 by a complete neighbourhood census and two independent SAT solvers;
also found a K5-free 18-vertex graph with only nine bad seven-sets.  The exact
value h(18) remains unresolved.
