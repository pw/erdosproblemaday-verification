# Erdős problem 1206: exact cube-Sidon table through 191

This bundle certifies every finite value of

```text
g3(N) = max{|I| : I subset [N] and {i^3 : i in I} is Sidon}
```

for `132 <= N <= 191`. Together with the preceding computation through 131,
the exact project table now ends at `g3(191)=159`.

This is finite computational progress only. It does not prove a linear
asymptotic lower bound and does not construct an infinite positive-density
set.

## Reproduce

Requirements are Python 3 and a C++17 compiler. No SAT, ILP, or third-party
Python package is used by the primary verifier.

```bash
./verify.sh
sha256sum -c SHA256SUMS
(cd hostile_audit && sha256sum -c SHA256SUMS)
```

The C++ verifier rebuilds every collision hypergraph from integer cube sums,
exhaustively proves all twelve lower endpoints, and directly checks explicit
upper witnesses. `audit_definition.py` independently reconstructs the
arithmetic and complementary Sidon sets. The `hostile_audit` directory records
a cold replay, independent integer-program optima, full nesting checks, and
search-semantic tests. CBC is corroborating evidence only; the dependency-free
exhaustive C++ verifier is the primary lower-bound proof artifact.
