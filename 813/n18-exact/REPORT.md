# Erdős problem 813: exhaustive order-18 exclusion

This is the compact publication copy of the continuation report. The complete
269 MB of raw sweep logs are included as `SWEEP_LOGS.tar.zst`, a 29 MB archive
bound by `OFFLINE_RAW_LOGS.sha256`. Small censuses, definition-level checkers,
audit summaries, the earlier d=11/d=12 bundle, and one replayable d=10 DRAT
spot proof are included beside this report.

## Result and exact confidence level

Write

\[
\alpha_3(G)=\max\{|S|:G[S]\text{ is triangle-free}\}.
\]

The remaining question was whether an 18-vertex graph can satisfy

\[
\omega(G)\leq4,\qquad \alpha_3(G)\leq6.                 \tag{1}
\]

An exhaustive exact-degree computation found no such graph.  The included
`tools/verify_w18_upper.py` independently checks an 18-vertex construction
with clique number five and a triangle in every seven-set.  Together these
give

\[
\boxed{h(18)=5}
\]

at **exhaustive solver-assertion level**.

The W18 checker has SHA256
`8ee0af91618b69113d49d54f3a7f24d6b043986b08e6e7252df622c60b940c1d`.
Its dependency-free `--witness-only` run verifies 100 edges, 223 triangles,
clique number five (on vertices 0,1,2,3,4), and maximum triangle-free induced
set order six.

That qualification is important.  The combinatorial reductions, census
coverage, CNF construction, and case-index coverage have definition-level
checkers.  Every remaining branch returned UNSAT, and selected difficult
branches have independently replayed DRAT certificates.  The millions of
individual d=9 and d=10 branch verdicts, however, do not each have retained
proof certificates.  Thus this is a high-confidence computer-assisted exact
result, not yet a single end-to-end independently replayable UNSAT proof.

## Human reductions

### Every candidate has maximum degree at least seven

Suppose `Delta <= 6`.  Brooks' theorem, applied componentwise, gives a proper
six-colouring: complete exceptions of chromatic number above six are excluded
by K5-freeness, and odd cycles need only three colours.  Five colours are
impossible because the union of the two largest colour classes has at least
eight vertices and is triangle-free.  Hence `chi=6`.

In a six-colouring, the union of any two colour classes is triangle-free, so
each such union has size at most six.  Since the six class sizes sum to 18,
all six classes have size three.

Fix a vertex `z`.  For any two of the five colour classes not containing `z`,
their six vertices together with `z` form a seven-set.  Its required triangle
must use `z` and one vertex from each class.  Thus `z` has a neighbour in every
other class, and every pair of other classes contains an adjacent pair of
`z`-neighbours.  Therefore `d(z)>=5`.  If `d(z)=5`, the five unique
representatives form a K5.  If `d(z)=6`, the neighbour counts are
`2,1,1,1,1`; the four singleton representatives, together with `z`, form a
K5.  Both are impossible, so `Delta>=7`.

The polished proof is `DELTA7_PROOF.md`, SHA256
`9381ef833c63bd21fcbb986ef14dc81948246fd7d9ce7e157b61bddc0cbeeb9a`.
Its brute-force boundary audit is `tools/delta7_check.py`, SHA256
`a7b630fa73f64eb17a4ff4eba28d3b72066eb0ab71035052187a950445c4881c`.

### Root-neighbourhood lemma

If four neighbours `A` of a vertex `v` are independent, put
`B=V-(N(v) union {v})`.  For every pair `x,y` in `B`, the seven-set
`{v} union A union {x,y}` can contain a triangle only if `xy` is an edge.
Hence `B` is a clique.  K5-freeness gives `|B|<=4`, so `d(v)>=13`.

Consequently, in every maximum-degree branch d=7,...,12,

\[
\alpha(G[N(v)])\leq3.                                  \tag{2}
\]

For an exact-degree root, (2) is represented by one clause for each four-set
`a,b,c,d` of neighbours:

`-va -vb -vc -vd ab ac ad bc bd cd`.

An independent auditor produced RUP derivations of these clauses from the
unstrengthened branch formula, using eleven additions per four-set.

### Root non-neighbour lemma for d at least nine

The root neighbourhood `H` is K4-free.  If `|H|>=9`, Ramsey's theorem
`R(4,3)=9` supplies an independent triple in `H`.  If the root non-neighbour
graph `M` also contained an independent triple, those two triples and the
root would form a triangle-free seven-set.  Therefore

\[
\alpha(M)\leq2\qquad(d\geq9).                           \tag{3}
\]

A self-contained proof of the Ramsey fact is enough here.  If the complement
of `H` were triangle-free with independence number at most three, every
degree would be at most three.  A vertex of degree at most two, together with
`R(3,3)=6` in its non-neighbours, gives an independent four-set.  Thus the
complement would be 3-regular on nine vertices, contradicting the handshaking
lemma.

The auditor also gave clean RUP prefixes deriving (2) and (3).  The clean
versions delete every lifted Ramsey intermediate before a solver's RAT proof
is appended:

| d | root-prefix SHA256 | clean M-prefix SHA256 |
|---:|---|---|
| 9 | `808935d3f22541eabbda6c3c35717ca751cc4a3e8603a91697306cec2d0153fe` | `7548b70acc027fabe3736ee5a6b774f6e3a6ed83da0926b2678ccc012589e717` |
| 10 | `7944f685346a711eda38b22494d241c9b6d76bd0c5ea554f932cabeba8992a83` | `50f4b8fb72c22e6796a8fe303b66185c6b566c9d5ee9f230c1f688591762c5a6` |
| 11 | `bbebc5c7f19fdad13ab62c17b8c6625ed7b53ea29bf8fe967c002e9b55355798` | `b1f4f880e719657f4f417bd293edcc8d723ae9aeab9ed08633b532d281f86829` |
| 12 | `470292eebdc1e1aa2015323cf14e9ede60050c77b81fd843f5bf2adb2483d563` | `7288610b5ad8e17890271f0b6ef81417bd184c97ea6277941fb2b9bc4596d364` |

## Exact maximum-degree CNF

For a maximum-degree branch `d`, relabel a maximum-degree vertex as 0 and its
neighbours as `1,...,d`.  The formula contains:

1. 153 edge variables and 816 triangle variables;
2. four clauses for each equivalence between a triangle variable and its
   three edges;
3. one negative ten-edge clause for every five-set, forbidding K5;
4. one positive 35-triangle clause for every seven-set;
5. a sequential at-most-d counter for the 17 incident edges at every vertex;
6. 17 units fixing `N(0)={1,...,d}`.

The natural part has 969 variables and 43,656 clauses.  The counters use
private auxiliary blocks.

`verify_degree_branch_cnf.py`, SHA256
`da3c03f42c3ae4dc619d6aa540c719031126b9c6d9fcfeb254903ad58c846d88`,
imports neither PySAT nor the generator.  It reconstructs every natural
clause, checks all root units and disjoint counter blocks, then existentially
projects a normalized sequential counter on all `2^17` Boolean inputs by
exact Horn closure.  It verified every branch d=6,...,12.

The four branch formulas used in the new exhaustion have SHA256 values:

| d | branch SHA256 |
|---:|---|
| 7 | `7d470e3c43cea962ee11e5a48d1018b84043bff68a68c7bd852b63d602675347` |
| 8 | `c5d863bafbd97bd398bf7da5442740edb003441be90146f3e1b99ec5a2401b97` |
| 9 | `e1c692e377b797393a0acb09f5f74091f3c5f9357aa484ff118d9d3a76ecca6a` |
| 10 | `2a63c718792ce7fdce0161a664ef5b39411241789430fbe6dce5af0264197618` |

## Complete canonical splits

Let `H=G[N(0)]`.  It is K4-free, and (2) gives ordinary independence
number at most three.  The exact canonical H census sizes are:

| d | 7 | 8 | 9 | 10 |
|---:|---:|---:|---:|---:|
| H types | 353 | 1,829 | 8,753 | 8,688 |

Their SHA256 values are, respectively,
`dcb9826f89febb23efdc2cce129faa588385a9f02211ac30a84e52906ee19739`,
`fff629fd92179ef4502f99548caed1481da39ac1239d3e99a78c6bbd3cba6df6`,
`c22b6fd0e5ebeea07afbf0396df30f153fbdc86c3374a95744d32100ffb9aa67`,
and
`4bfaf9ddb556254347a6dee7200b4852696686257427c107c6ab7cd2421177f0`.

`verify_alpha3_filtered_census.py` checks that these are exactly the ordered
alpha-at-most-three sublists of the complete K4-free, triangle-independence
at-most-six neighbourhood censuses.  Its SHA256 is
`d16eac14cb2b87afff0948665bd944a8f4b0edbdf49de5eaf695e2dcd8aea66c`;
the combined verification log has SHA256
`8fe2f696462b6ebfbfc8729dc012adfad5f3a9e5fcb0ccab33ca6b98188163f3`.

As a further completeness control, fresh `nauty-geng` runs over all 1,044,
12,346, and 274,668 unlabeled graphs of orders 7, 8, and 9 were filtered from
the definitions and canonicalized with `shortg`.  Their canonical sets agree
byte-for-byte with the three parent censuses.  The frozen order-10 census had
already been independently reproduced from all 12,005,168 unlabeled graphs.

For d=9 and d=10, (3) also permits a split by `M`, independently of the H
labelling:

| d | order of M | canonical M types | SHA256 |
|---:|---:|---:|---|
| 9 | 8 | 179 | `a7a0679d89af8f93e3008e4bc3ecb9f3f870a00fb5759720ddf617141b0e1e51` |
| 10 | 7 | 71 | `64037dfeb6abc2f64fa92afc792e827d65325bc093434b8a7f9a906ae217bf29` |

The order-7 census was checked against all `2^21` labelled graphs: exactly
113,949 valid masks form the 71 disjoint isomorphism orbits.  The order-8
census was generated in two independent directions: direct filtering of all
12,346 order-8 graphs, and complementing all 410 triangle-free order-8 types
whose independence number is at most four.  Both routes leave 179 types and
give the same canonical `shortg` bytes, SHA256
`7c760244e3efd2ef7549def2792490108155a1adcd8311ad4a2099c4d68799d8`.

## Exhaustive UNSAT results

Each H-only case fixes all edges inside `H` as signed assumptions.  Each
product case fixes all edges inside both `M` and `H`; all cross-edges remain
free.  A persistent CaDiCaL 1.9.5 instance was used per shard.  Learned
clauses under IPASIR assumptions remain consequences of the shared base.

| maximum degree | split | branches | verdict | wall time |
|---:|---|---:|---|---:|
| 7 | H | 353 | all UNSAT | 23.231 s |
| 8 | H | 1,829 | all UNSAT | 164.810 s max over 2 shards |
| 9 | M x H | 1,566,787 | all UNSAT | 75.556 s max over 7 shards |
| 10 | M x H | 616,848 | all UNSAT | 326.375 s max over 7 shards |

The coverage audits report:

```text
VERIFIED census=...census_n7_alpha3.g6 logs=1 shard_done=1 unique_cases=353 expected=353 all_UNSAT=YES
VERIFIED census=...census_n8_alpha3.g6 logs=2 shard_done=2 unique_cases=1829 expected=1829 all_UNSAT=YES
VERIFIED logs=7 shard_done=7 unique_pairs=1566787 expected=1566787 all_UNSAT=YES
VERIFIED logs=7 shard_done=7 unique_pairs=616848 expected=616848 all_UNSAT=YES
```

The four audit-log SHA256 values are:

```text
888c1693c94b9371562514b303b868c32712707081bc261b75e5462294e0c99f  audit_d7_alpha3_census.log
869eab82e137b0b10201b399dc9f7a6bcbb77eb77ecd58a3d54216f5a515533e  audit_d8_alpha3_census.log
eaea829c0e46ae693c217a46425df9cada1e4a0e8ac50b48cc58e9f0c99f1e75  audit_d9_double_census.log
e8ac9ce37c82c5a551c99163da2dd3f8e7f75e71de96076a3fb4d310a34e6b27  audit_d10_double_census.log
```

For d=11 and d=12, the frozen earlier bundle exhausts all 403 and 8 complete
neighbourhood types.  Both CaDiCaL and Kissat returned UNSAT in all 411
cases.  The order-13 census is empty, so degree at least 13 is impossible.

This covers every degree:

- d at most 6 is excluded by the colouring argument;
- d=7,8,9,10 is excluded by the new exact branch sweeps;
- d=11,12 is excluded by the earlier two-solver census;
- d at least 13 is excluded by the complete neighbourhood census.

Therefore no graph satisfying (1) exists.

## Independent proof-certified spot checks

For the slowest or otherwise difficult representatives, the exact assumptions
were materialized as unit clauses in standalone DIMACS files.  Independent
checkers verified the base prefix and every signed unit.  External Kissat then
returned UNSAT and `drat-trim` replayed every proof with `s VERIFIED`:

| branch | Kissat DRAT SHA256 | drat-trim log SHA256 |
|---|---|---|
| d7 H case 344 | `ad71232fe98132d618ce1c0262c41bbffe8132370b4141a34cd7936cc9e2ced2` | `bab10487dfb1134a76e090ffb4ccf13f9465be5a79620e94bbc6b9dff2c68063` |
| d8 H case 1820 | `f92c52ae431b9401d79ea1e51315a8c60df49124586b816213976d915a04d4af` | `81432f63c926a03f67ee2a4dd5828c35ca3e7ba340fadd96354e592cc85fe6c5` |
| d9 flat 730156 = M83/H3657 | `9cc426d304dc67b29e8c18a833ac83bf3cfb32a38ed9635754c193162336b188` | `9d742aef823002b618f97db03831d94a82a958f1ce1027fa349a7d23a22d29e6` |
| d10 flat 512188 = M58/H8284 | `611f4be57e9eacd076042d42dd203a2b92e1415ab5d03c6ee6aadedbbdf98941` | `feb322d3aaa30b203180fb13c0185f654c082e0591233895306fc3ac5acc2d43` |

These replayable cases cross-check the encoding and the persistent-solver
path, but they are not certificates for all branches.

## Proof-production attempts and retractions

Proof-producing root-only d=10, d=11, and d=12 formulas strengthened by the
two RUP lemmas each reached a 1,800-second timeout.  Their partial binary DRAT
files contain no terminal empty-clause proof and make no claim.  Only the
clean prefixes listed above should be used in any later proof composition;
older lifted-M prefixes retained Ramsey intermediates and are unsuitable to
prepend before arbitrary RAT steps because RAT is not monotone under added
clauses.

An early `branch_d10_three_tf6.cnf` pilot is also **retracted**.  It fixed a
maximum-degree root and a prescribed three-partition simultaneously, which is
not jointly without loss of generality.  It excluded only that special
distribution.  The correct fully symmetric natural formula, with no root or
degree units and exactly 60 triangle-false units for three prescribed
six-sets, is a separate experiment and does not enter the result above.

## Central reproducibility artifacts

- `degree_double_census_incremental.py`: generic d=9/d=10 product runner,
  SHA256
  `3011a1901794cc5994a168516fce8be74a41de791509c4edf1b7fd2070f7f2e0`;
- `d10_double_census_incremental.py`: original d=10 product runner, SHA256
  `6f7f2bdcb7db0f6dcefcc11fb28e1acd356bd5dae3cd3d1d23d5c9288f3f047c`;
- `audit_double_census_logs.py`: exact flat-index auditor, SHA256
  `df5863c50545b60e583822124dbc12a786cf35712e05ed1a8943d78c3f341855`;
- `audit_degree_census_logs.py`: H-case coverage auditor, SHA256
  `b171d6cc4bf72577433e9766f499fafa8aadedad57cb404918bd90cd0a044301`;
- `make_double_census_case_cnf.py` and
  `verify_double_census_case_cnf.py`: standalone product-case proof mapping,
  SHA256 values
  `7e01e7a8e2cff6dd551597dc3b1eba3b2ce9a6c706a0fae3993a4e9ba05430da`
  and
  `3a8a27aa64fe02ef260bd16667cb00fd7a786bf79d248fa3471cf0a5213fa2d2`;
- the complete raw shard logs and all four branch CNFs are retained in the
  full offline bundle and bound here by `OFFLINE_RAW_LOGS.sha256` and
  `OFFLINE_BRANCH_CNFS.sha256`; compact audit outputs and a replayable d=10
  spot case are included locally.
