# Problem 149: exact degree-4 strong clique number

This package audits the literature-derived finite statement

```text
max { omega(L(G)^2) : G finite simple, Delta(G) <= 4 } = 20.
```

The upper bound is the degree-4 specialization of Kumar, Mohar, and
Pragada's July 2026 arXiv preprint. Its v1 proof contains a malformed
auxiliary interval. Both the author report and hostile audit disclose the
problem and reconstruct the argument with the fixed constant
`beta=620/1987`; exact rational checks verify every displayed identity and
the required polynomial positivity. The conversion to the general strong
clique coefficient uses the named published theorem of Faron and Postle.

Equality is attained by the independent two-vertex blowup of `C5`. It has
maximum degree 4 and 20 edges, and every pair of edges is at distance at most
2 in the line graph. Two dependency-free implementations check the graph and
the constant argument.

This does **not** settle the strong chromatic index in Problem 149. The exact
justified coloring range remains

```text
20 <= max { chi(L(G)^2) : Delta(G) <= 4 } <= 21.
```

The same KMP preprint already appears in the site's Problem 934 work, but
there it is used for the separate `L(G)^3` degree-diameter problem. The
Section 2 coefficient, its degree-4 consequence, and Problem 149 were not
previously treated. This overlap is explicit in both reports.

Run `./reproduce.sh` for manifest and independent algebra/graph checks. The
author's prepublication absence script is intentionally not rerun: its input
is the mutable site tree, and publication itself makes its zero-reference
condition false. Two audit snapshots of that tree are also omitted because
one contains unrelated uncommitted ledger work; their hashes remain bound by
the preserved audit manifest.

Classification: **PARTIAL**, literature-derived, with the parent coloring
conjecture still open.
