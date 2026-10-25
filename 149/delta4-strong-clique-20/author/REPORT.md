# Erdős Problem 149: exact strong-clique value at Delta 4

Access and audit date: 2026-08-11 UTC.

## Outcome

This is a literature-derived partial, not our discovery and not a solution of
Problem 149.

Let

```text
Omega_4 = max { omega(L(G)^2) : G finite simple, Delta(G) <= 4 },
X_4     = max { chi(L(G)^2)   : G finite simple, Delta(G) <= 4 }.
```

The audited exact result is

```text
Omega_4 = 20.
```

For the strong chromatic index, only

```text
20 <= X_4 <= 21
```

is justified. In particular, the Erdős-Nesetril coloring conjecture at
maximum degree 4 remains open.

## Live-page gate

The rendered Problem 149 page, LaTeX view, and discussion were captured
through the Bright Data browser. At access time the page displayed:

- status `OPEN`;
- `0 claimed proofs for this problem`;
- `Currently working on this problem: None`;
- `Interested in collaborating: None`.

The live statement asks whether every graph of maximum degree `Delta` has
strong chromatic index at most `(5/4)Delta^2`. The page records the known
Delta-4 upper bound 21 and says that even the corresponding strong-clique
bound `(5/4)Delta^2` is open. Its listed general strong-clique coefficient is
the older `4/3` bound.

## Primary theorem and exact specialization

Kumar, Mohar, and Pragada, arXiv:2607.02698v1 (2 July 2026), Corollary 1.7,
prove for every finite simple graph `G` that

```text
omega(L(G)^2) <= (2607/1987) Delta(G)^2.
```

At maximum degree 4 the exact rational bound is

```text
16*2607/1987 = 41712/1987 = 21 - 15/1987 < 21.
```

Since clique number is integral, `omega(L(G)^2) <= 20`.

The arXiv v1 proof contains a genuine auxiliary-definition typo: its
`beta*` interval is printed as `[0,1/4]`, although the surrounding argument
proves `beta*>1/4`. `PROOF_AUDIT.md` discloses this and reconstructs the
induction with the fixed constant `beta=620/1987`; the verifier checks the
paper's sum-of-a-square identity, negative discriminant, and final polynomial
identity exactly. The conversion to the general coefficient remains modulo
the explicitly named Faron-Postle 2019 conditional theorem, whose primary
source is bundled.

## Equality

The standard blowup `C5^(2)` has five independent parts of size 2, with all
four edges inserted between consecutive parts. It is 4-regular and has 20
edges. Direct enumeration proves every pair of its edges is at line-graph
distance at most 2, so

```text
L(C5^(2))^2 = K20.
```

Thus `Omega_4 >= 20`, establishing equality with the upper bound. The
dependency-free checker also verifies the general `C5^(t)` formulas for
`1 <= t <= 8` and recomputes the Delta-4 edge list from definitions.

## Coloring boundary

For the extremal blowup, the complete line-graph square forces 20 colors, so
`X_4 >= 20`. Huang, Santana, and Yu (Electronic Journal of Combinatorics,
2018), Theorem 2, prove every graph of maximum degree 4 has a strong edge
coloring with at most 21 colors. Hence `X_4 <= 21`.

The strong-clique theorem cannot replace 21 by 20: in general
`omega(Q) <= chi(Q)`, not conversely.

## Local novelty and overlap disclosure

The corrected two-schema scanner confirms that Problem 149 is absent from
both local site articles and the ledger. Neither the coefficient `2607/1987`
nor KMP Corollary 1.7 appears locally.

There is a same-paper overlap that must be explicit. Ledger Problem 934
already cites and audits arXiv:2607.02698, but it treats the separate Section
3 degree-diameter problem `h_3`, equivalently the `L(G)^3` framework. It does
not treat the Section 2 strong-clique coefficient, its Delta-4 rounding, or
Problem 149. Thus the exact theorem here is locally new, while the source
paper itself is not untouched.

## Trust boundary

- Live metadata is a dated rendered-page observation.
- The rounding, polynomial identities, graph construction, degrees, edge
  count, and all line-graph distances are exact and dependency-free.
- KMP Theorem 1.6 was reconstructed with its fixed constant after correcting
  the printed interval typo.
- The general-clique reduction relies on Faron-Postle Theorem 1.9 as a named
  published theorem.
- The coloring upper bound relies on Huang-Santana-Yu Theorem 2.
- No formal proof assistant checks these named theorems.

## Reproduction

Run:

```bash
./run_all.sh
```

Expected final line:

```text
ALL CHECKS PASSED
```

Final classification:

```text
PARTIAL: The new general strong-clique theorem implies the exact value
Omega_4=20, attained by C5^(2); the strong chromatic maximum remains 20 or 21,
so Problem 149 remains open.
```
