# Provenance and claim boundary

The new theorem-bearing object is `q9_edges_1531.json`.  Its correctness does
not depend on the heuristic that found it, the predecessor certificates, or
any literature claim.

The public comparison is deliberately narrow:

- `provenance/q9_public_1505.json` is the explicit 1505-edge certificate at
  public repository commit `74e84382cbbc20b32a2ac679bff977cad3ac5d24`.
- `provenance/q9_edges_1506.json` is the independently audited certificate
  published by Erdos Problem a Day earlier on 2026-08-11.

Their hashes are checked by the manifest and printed by
`compare_frontiers.py`.  The 1531-edge graph improves both identified
certificates.  Searches of the contemporaneous Problem 86 page, forum, OEIS
A245762, the Minamoto preprint, and the identified construction repository
had found no larger public Q9 edge list before this search.  That negative
search cannot exclude private, unindexed, or simultaneous work, so no
unconditional priority claim is made.

The live Problem 86 page was OPEN with zero claimed proofs and no current
worker when the preceding 1506 package was frozen.  The parent asymptotic
problem remains open.  This bundle claims only `ex(Q_9,C_4)>=1531`.

The copied generator is MIT-licensed; its license is preserved in
`provenance/LICENSE`.  No third-party paper PDF is needed for or included in
this certificate bundle.
