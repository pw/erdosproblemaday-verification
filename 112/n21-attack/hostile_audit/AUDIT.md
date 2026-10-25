# Hostile audit: Erdős problem 112, order 21 bundle

Audit date: 2026-08-12 UTC

Audited input: `/tmp/erdos112_n21`

## Verdict

The bundle's three rigorous claims pass:

1. the six root profiles are a complete split, assuming the already
   established value `k(3,3)=9`;
2. the frozen order-21 state has exactly one independent triple and no
   transitive four-tournament;
3. none of the eight listed cyclic order-20 witnesses extends unchanged by
   one vertex.

No unrestricted order-21 SAT or UNSAT conclusion is supported or claimed.
The certified interval remains `21 <= k(3,4) <= 25`.

Run the independent standard-library audit with:

```bash
python3 audit_112_n21.py
```

It does not import the producer's checker.  Its transitivity test enumerates
linear orders, and its extension proof uses a generic ternary CSP with dynamic
variable ordering instead of the producer's fixed-order recursion.

## Root-profile completeness

For a root `v`, a transitive triple in either directed neighbourhood extends
with `v` to a transitive four-set, while an independent triple remains
independent.  Thus `|N+(v)|,|N-(v)| <= 8` from `k(3,3)=9`.
Two non-neighbours of `v` cannot be nonadjacent, so `I(v)` induces a
tournament.  Every tournament on eight vertices contains a transitive
four-set: take a four-vertex in- or out-neighbourhood of a vertex and use the
elementary fact that every four-vertex tournament contains a transitive
triple.  Hence `|I(v)| <= 7`.

The three sizes sum to 20.  Global arc reversal permits `out >= in`, leaving
exactly

```text
(8,8,4), (8,7,5), (8,6,6), (7,7,6), (8,5,7), (7,6,7).
```

Relabelling the three root classes as consecutive blocks loses nothing, so
the six generated profile instances cover every hypothetical witness.

Source inspection also confirmed the ternary CNF is definition-exact:
exactly one state per unordered pair, one no-independent-triple clause per
triple, all 24 possible topological orders excluded per four-set, correct root
units, and valid local degree bounds.  Rebuilding all six profiles gave
6,573 variables and 158,010 clauses each.

## Near witness

An independently written decoder and permutation-based obstruction test gave:

```text
arcs                         137
nonedges                      73
independent triples            1: (5,13,16)
transitive 4-tournaments       0
profile histogram
  (6,6,8): 3
  (6,7,7): 7
  (7,6,7): 7
  (7,7,6): 4
state SHA-256
  6be5046ca0dc52cbea5a6127f6f7ea8879831b7b5e325fe03b9a7955838cfa6f
```

In particular, vertices 5, 13, and 16 are exactly the nondegree-eight
vertices, as claimed.

## Exact extension audit

The producer checks only obstructions containing the new vertex, so this
audit first checked the omitted premise directly.  Every listed cyclic base
has 120 arcs, constant `(out,in,non)=(6,6,7)`, no independent triple, and no
transitive four-tournament.

For each base the independent audit then constructs the exact 20-variable
ternary extension CSP:

- 70 binary constraints forbid making the new vertex nonadjacent to both
  endpoints of an old nonedge;
- 180 old transitive triples each contribute exactly four forbidden relation
  patterns, the four possible insertion ranks of the new vertex.

These 250 constraints are precisely all new obstructions.  The backtracker
branches over all remaining values and prunes only a fully assigned explicit
constraint.  It found no satisfying assignment in every case, visiting
66--81 dynamically ordered nodes.  A fresh run of the producer's fixed-order
checker reproduced its 1,907--10,598 node counts.  A separate CaDiCaL run also
returned UNSAT for all eight, but that unlogged solver result is corroboration,
not part of the proof.

## Checker hardening before freezing

Two small omissions in the producer checker do not invalidate the results,
because this audit independently verified the underlying facts, but should be
patched in the publication copy:

- `verify_near_witness()` prints `arcs=137 nonedges=73` as hard-coded text;
  it should compute and assert the two counts.
- `verify_extension_instances()` should assert that each old cyclic graph has
  no independent triple and no transitive four-set before relying on the fact
  that every new obstruction is anchored at vertex 20.

The bounded Hamming-ball and local-search statements have no proof logs.  The
report labels them computational diagnostics and does not use them in a
mathematical conclusion; that qualification is necessary and adequate.
