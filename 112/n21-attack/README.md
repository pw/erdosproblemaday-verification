# Order-21 search bundle for Erdős problem 112

The rigorous, quick entry point is:

```bash
python3 verify_n21_artifacts.py
```

It verifies the six-profile reduction, the concrete one-defect near witness,
and exact nonextendability of all eight known cyclic order-20 witnesses.
The checker computes the near-state edge counts and first verifies that each
fixed order-20 base is itself obstruction-free before exhausting its
extensions.

`hostile_audit/` contains an independent definition-level implementation. It
uses permutation-based transitivity and a dynamic ternary constraint search;
it reproduces the near witness and proves all eight extension instances
unsatisfiable in 66--81 search nodes.

Search infrastructure:

- `generate_n21_cnf.py`: lossless ternary CNF for one of the six profiles;
- `solve_profile.py`: PySAT/Kissat or CaDiCaL driver;
- `n21_local_search.cpp`: breakout/tabu ternary local search;
- `test_d20_extensions.py`: separate SAT extension check;
- `near_d20_search.py`: bounded-distance search around cyclic witnesses;
- `repair_best_near.py`: bounded-distance exact repair of a score-one state;
- `solve_restricted_profile.py`: exploratory template restrictions.

No full-profile solver run completed, and no solver proof log is included.
Accordingly this bundle makes no unrestricted SAT or UNSAT claim at order 21.
