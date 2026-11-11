# Erdős #488: counterexample and exact statement adapter

This self-contained Lean file includes the finite smooth-number counterexample and a proved adapter to the exact proposition in `google-deepmind/formal-conjectures/FormalConjectures/ErdosProblems/488.lean` as read on 5 September 2026. It excludes generators0 and1, uses `Finset.max`, and compares rational densities.

The mathematical work and this package were produced with GPT-6 Astra in Codex, directed by Declan Gessel. Independent specialist review and priority checking are being sought. The earlier counterexample was verified by Jig: https://jig.so/p/398?s=40 . Exact server run: https://github.com/WoshuaJolk/jig-verifier/actions/runs/33990129375 .

## Reproduce

Save all files in one directory, install Lean using elan, and run:

```sh
lake update
lake exe cache get Mathlib.NumberTheory.SmoothNumbers Mathlib.Data.Nat.Totient Mathlib.Algebra.Order.BigOperators.Group.Finset Mathlib.Tactic.NormNum Mathlib.Tactic.Linarith Mathlib.Data.Nat.Factorization.Basic Mathlib.Data.Fintype.Card Mathlib.Data.Fintype.BigOperators Mathlib.Order.Interval.Finset.Nat Mathlib.Tactic.ByContra Mathlib.Data.Nat.GCD.BigOperators Mathlib.Data.Finset.Max Mathlib.Tactic.Tauto
lake env lean Erdos488.lean
```

The declaration `Erdos488ExactAdapter.refutation : ¬ Erdos488ExactAdapter.proposition` matches the full right side of the collection's `erdos_488`. The print-axioms commands report only `propext`, `Classical.choice`, and `Quot.sound`. There are no admitted results or custom axioms. The constructor establishes an index k<4096 by finite existence; its value is not enumerated.

The collection update should set `answer(False)` and retain its full proposition. This external proof avoids placing a long proof in the statement collection.
