# Erdős #432 finite exact extension

This bundle certifies the exact two-row thresholds `L_11,...,L_40`, extending
the prior table `L_2,...,L_10` and the prior bound `L_11>100`.

Reproduce the independent audits:

```bash
g++ -O3 -std=c++17 -Wall -Wextra -pedantic audit_clique.cpp -o audit_clique
./audit_clique

python3 audit_cpsat.py
```

The Python audit requires OR-Tools.  The C++ audit has no nonstandard
dependency.

See `REPORT.md` for definitions, the exact table, proof of completeness, live
collision gate, and claim boundary.

`parse_report.py` mechanically confirms that the 30 table rows in the report
are identical to the rows embedded independently in both audit programs.
