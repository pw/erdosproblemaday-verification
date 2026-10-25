# Problem 1183 exact `f(7)` and `F(7)` certificate

This bundle certifies the finite computer-assisted result `f(7)=4`, `F(7)=7`.

Contents:

- `REPORT.md` — complete proof and scope;
- `verify_1183_f7.py` — standard-library definition checker and independent
  exact upper search;
- `lower_core.cnf` — 42,035-clause lower-bound core;
- `lower_core.drat` — binary DRAT proof;
- `drat-trim` — x86-64 proof checker;
- `VERIFY_OUTPUT.txt`, `DRAT_REPLAY.txt` — frozen outputs;
- `audit_lattice_upper.cpp`, `AUDIT_LATTICE_OUTPUT.txt` — independent direct
  enumeration for the lattice-closed upper bound;
- `LIVE_PAGE.txt`, `LIVE_FORUM.txt` — 2026-08-12 collision gate;
- `SHA256SUMS` — closed integrity manifest.

Reproduce with `./reproduce.sh`. Ordinary assertion-enabled Python is required;
do not invoke the checker with `python3 -O`.
