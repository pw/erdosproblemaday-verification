# v1.1 `InventoryNonzero`: built on our machine (2026-10-28)

Gap 2 of our review: `OneHighFamilyV2CheckedUnsat` carries a `nonzero` field (no literal 0 in any clause) that the
reviewed commit never proved. v1.1 (Zenodo 23519149, tag erdos85-paper-v1.1 = f59a077decfe) adds
`Proofs/Erdos85OneHighV2InventoryNonzero.lean` (sha256 53294fd6…2c89), a structural proof for every table.

What we did: built that module and its whole import cone, 190 project modules + 1 Archive module (`cone.txt`), with
our own driver (`drive_v11.py`: one `lean -j1` per module in dependency order into an EMPTY output root; Lean 4.31.0;
Mathlib and package oleans from the pinned `lake exe cache get`). All 191 compiled with rc 0 (`steps.tsv`; one module,
InventoryOrbitCheck, was killed once by OUR memory watchdog while another tenant held the RAM and passed on re-run,
963 s). The module's own `#print axioms` lines (`Proofs.Erdos85OneHighV2InventoryNonzero.log`):

- `oneHighFamilyV2Clauses_nonzero`: propext, Quot.sound
- `oneHighCapacityInventory_nonzero`: propext, Classical.choice, Quot.sound
- `oneHighFamilyV2CheckedUnsat_of_unsat`: propext, Quot.sound
- `oneHighCapacityInventory_checked_of_unsat`: propext, Classical.choice, Quot.sound

No `native_decide`, `decide` or `sorry` in the file (read). Scope: a compile-time kernel check against the cached
Mathlib oleans; NOT `leanchecker --fresh` (which would also re-check every imported .olean). The two unused-simp-argument
warnings are linter warnings. The `.lake` trees were deleted afterwards (disk guard).
