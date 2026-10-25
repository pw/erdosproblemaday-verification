# Proof audit

## Claim being audited

For every finite simple graph `G` with maximum degree at most 4,

```text
omega(L(G)^2) <= 20,
```

and equality is attained.

The upper bound is a corollary of Kumar-Mohar-Pragada (KMP), not a new general
bound proved here. The arithmetic specialization and equality construction
are independently checked.

## Source typo

In arXiv:2607.02698v1, Section 2 defines

```text
beta* = min { beta in [0,1/4] : P_beta(x) >= 0 for all x >= 0 }.
```

The preceding sentence proves `P_beta(1) < 0` whenever `beta <= 1/4`, and the
next lemma claims `beta* > 1/4`. Thus `[0,1/4]` is a typographical error and
the displayed definition is empty as written.

The proof does not need `beta*`. Fix

```text
beta = 620/1987.
```

The paper's exact decomposition is

```text
P_beta(x)
 = beta (x^2 - (747/1240)x - 211/1000)^2
 + (708654527125 x^2 - 1203303717450 x + 510806838853)
   / 6119661950000.
```

The second quadratic has positive leading coefficient and discriminant

```text
-2478929365735048000 < 0.
```

Hence `P_beta(x) >= 0` for every real `x`. The verifier checks the polynomial
identity and discriminant with exact rational/integer arithmetic.

## Fixed-beta reconstruction of KMP Lemma 2.2

Let `H` be a nonempty bipartite subgraph of `G`, with `E(H)` a clique in
`L(G)^2`. Put `sigma = sigma_G(H)` and `Delta = Delta(H)`. Induct on
`|E(H)|` to prove

```text
|E(H)| <= beta sigma^2.                                      (1)
```

For the base case, `sigma >= 2` and `beta > 1/4`.

Choose a vertex `v` of `H`-degree `Delta`. With `v` on the `X` side of a
bipartition, set

```text
A = N_H(v),
C = N_G(v) minus A,
B = V(H) minus N_G[v],
F = H[B].
```

The counting in the paper gives

```text
|E(H)| <= Delta(sigma-Delta) + (1/Delta) sum_{x in B cap X} h_x f_x,  (2)
```

where `h_x = |N_H(x) cap A|` and `f_x = deg_F(x)`. The key facts were checked
against the definitions:

- every `F` edge and every edge `va` must be joined within two steps in the
  line graph, so each `a in A` is adjacent to an endpoint of that `F` edge;
- therefore `sigma_{G[B]}(F) <= sigma-Delta`;
- `sum h_x <= Delta^2` and, by induction, `sum f_x = |E(F)| <=
  beta(sigma-Delta)^2`;
- `h_x+f_x <= Delta`.

With

```text
p = beta(sigma-Delta)^2 / (Delta^2 + beta(sigma-Delta)^2),
q = 1-p,
```

the identity

```text
(p^2 h + q^2 f)(h+f) - hf = (ph-qf)^2
```

turns (2) into

```text
|E(H)| <= Delta(sigma-Delta)
          + Delta^2 beta(sigma-Delta)^2
            / (Delta^2 + beta(sigma-Delta)^2).               (3)
```

Set `t=Delta/sigma`, which lies strictly between 0 and 1. After division by
`sigma^2`, the right side of (3) is

```text
F(t) = t(1-t) + beta t^2(1-t)^2 / (t^2 + beta(1-t)^2).
```

Exact clearing of denominators gives

```text
beta - F(t)
 = (1-t)^4 P_beta(t/(1-t)) / (t^2 + beta(1-t)^2) >= 0.
```

The verifier checks this polynomial identity exactly. This proves (1) with
the fixed `beta`, avoiding the malformed `beta*` definition.

## General strong-clique coefficient

Faron-Postle Theorem 1.9, quoted as KMP Theorem 1.5, converts (1) into

```text
|E(J)| <= ((1+beta)/4) sigma_G(J)^2
```

for a general strong clique `E(J)`. Since `sigma_G(J) <= 2 Delta(G)`,

```text
omega(L(G)^2) <= (1+beta) Delta(G)^2
                = (2607/1987) Delta(G)^2.                    (4)
```

This step remains rigorous modulo the named Faron-Postle theorem. Its primary
PDF and TeX source are bundled and its quantifiers and coefficient were
checked directly.

## Exact Delta=4 rounding

At `Delta(G) <= 4`, (4) gives

```text
omega(L(G)^2) <= 16*2607/1987 = 41712/1987
                                      = 21 - 15/1987 < 21.
```

Clique number is an integer, so it is at most 20.

## Equality construction

Replace every vertex of `C5` by an independent 2-set and every cycle edge by
the complete bipartite graph between its two parts. The resulting graph has
10 vertices, degree 4, and 20 edges. Every two edges have line-graph distance
at most 2, so `L(G)^2 = K20`. The standalone verifier constructs the graph and
checks all 190 edge pairs; 60 pairs have line distance 1 and 130 have distance
2. Therefore its strong clique number and strong chromatic index are both 20.

Combining upper and lower bounds proves the exact strong-clique value 20.

## What is not proved

Clique number is only a lower bound for chromatic number. Huang-Santana-Yu
prove the latter is at most 21 for maximum degree 4, so the current exact
coloring interval is

```text
20 <= max chi(L(G)^2) <= 21.
```

No step in this audit improves 21 to 20. Problem 149 remains open.
