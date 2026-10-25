# Problem 80 finite extension: exact order nine

This frozen bundle verifies

\[
(M_0(9),M_1(9),\ldots,M_7(9))=(0,18,21,27,28,30,32,36),
\]

where (M_k(n)) is the largest edge count of an (n)-vertex graph in which
every edge lies in a triangle and every edge lies in at most (k) triangles.

The result is a finite computational extension, not a solution of the
asymptotic Erdős problem and not a novelty claim.

Files:

- `REPORT.md`: statement, elementary arguments, collision audit, and scope;
- `producer.py` / `producer.out`: SAT witnesses and the two UNSAT boundaries;
- `independent_scan.cpp` / `independent_scan.out`: full unlabelled census;
- `audit.py` / `audit.out`: separate NetworkX definition-level audit;
- `all_n9.g6`: frozen 274,668-record nauty stream;
- `sources/`: Bright Data live captures and OEIS/arXiv source records;
- `reproduce.sh`: end-to-end single-core reproduction.

Run `./reproduce.sh` for the full check.
