# Hostile audit: Erdos Problem 149, Delta = 4

Audit time: 2026-08-11 UTC.

Reviewed bundle:

`../problem149_delta4_strong_clique_exact_20260811`

## Verdict

`PASS`, but only for the following publication-safe statement:

> **Literature-derived corollary, not an original result.** For finite simple
> graphs,
> \[
> \max_{\Delta(G)\le 4}\omega(L(G)^2)=20.
> \]
> The upper bound follows from Kumar--Mohar--Pragada,
> arXiv:2607.02698v1, Corollary 1.7, after repairing the disclosed malformed
> auxiliary definition in its proof. Equality is attained by the independent
> 2-blowup of `C5`.

`GAP/OPEN` for Erdos Problem 149 itself. That problem is about the strong
chromatic index, not the strong clique index. The justified finite-simple-graph
statement is only

\[
20\le \max_{\Delta(G)\le4}\chi(L(G)^2)\le21.
\]

It is not publication-safe to call the bundle a solution of Problem 149, to
claim the maximum strong chromatic index is 20, or to present the exact clique
value as a new discovery.

## 1. Definitions and scope

For a finite simple graph `G`:

- `L(G)` has one vertex for every edge of `G`; two are adjacent exactly when
  the corresponding edges share an endpoint.
- `L(G)^2` joins distinct vertices whose distance in `L(G)` is at most 2.
- A strong edge coloring of `G` is a proper vertex coloring of `L(G)^2`.
  Thus the strong chromatic index is `chi(L(G)^2)`.
- A strong clique is a set of edges pairwise at line-graph distance at most 2.
  Its maximum size is `omega(L(G)^2)`, the strong clique index.

Always `omega(Q) <= chi(Q)`. An upper bound on `omega(L(G)^2)` therefore does
not give the same upper bound on `chi(L(G)^2)`.

Define

\[
\Omega_4=\max\{\omega(L(G)^2):G\text{ finite simple},\ \Delta(G)\le4\}
\]

and define `X_4` analogously with `chi` in place of `omega`. The audited result
is `Omega_4 = 20`; only `20 <= X_4 <= 21` is established.

## 2. Current provenance

I independently refetched the rendered problem and forum pages through Bright
Data. At audit time they showed `OPEN`, four comments, zero claimed proofs, no
current worker, and no collaboration marker. The page was last edited 10 April
2026, before the KMP preprint, and still lists the old `4/3` clique coefficient.
That text is stale literature context, not contrary evidence against KMP.

The live arXiv record for KMP had only version 1, submitted 2 July 2026. Fresh
downloads matched the bundle byte for byte:

```text
29aee6e2b4269210a02c98287cb3798591ef0dc1d16439f5befdb309d47bf115  e-print source
bf79c035f6eced5515c84d248de73ec03f24a5198d27c62c4adff033a4608153  PDF
```

Fresh downloads of Faron--Postle arXiv:1708.02264v1 and the official
Huang--Santana--Yu PDF also exactly matched the bundled files. KMP is currently
an arXiv v1 preprint, not a refereed publication; that status should remain
visible in any article.

Primary links:

- KMP: <https://arxiv.org/abs/2607.02698>
- Faron--Postle: <https://arxiv.org/abs/1708.02264>, published as J. Graph
  Theory 92 (2019), 261--274, DOI 10.1002/jgt.22452.
- Huang--Santana--Yu: <https://doi.org/10.37236/7016>.
- Problem 149: <https://www.erdosproblems.com/149>.

## 3. KMP quantifiers and the source typo

KMP's opening convention is finite simple graphs. Theorem 1.6 says that for
every graph `G` and every bipartite subgraph `H` whose edges form a clique in
`L(G)^2`,

\[
|E(H)|\le \frac{620}{1987}\sigma_G(H)^2,
\qquad
\sigma_G(H)=\max_{xy\in E(H)}(d_G(x)+d_G(y)).
\]

Corollary 1.7 is quantified over every graph and states

\[
\omega(L(G)^2)\le\frac{2607}{1987}\Delta(G)^2.
\]

The v1 proof does contain a real defect as printed. It defines

\[
\beta^*=\min\{\beta\in[0,1/4]:P_\beta(x)\ge0\text{ for all }x\ge0\},
\]

but `P_beta(1) = 4 beta^2 + 2 beta - 1 < 0` throughout that interval.
Consequently the displayed set is empty and `beta*` is undefined. This cannot
be silently quoted as a valid definition.

The defect is repairable without optimizing or defining `beta*`: fix

\[
\beta_0=\frac{620}{1987},\qquad \frac14<\beta_0<\frac13.
\]

Every later use of `beta*` in Lemma 2.2 needs only (i) `beta > 1/4` for the
one-edge base case and (ii) `P_beta(x) >= 0` for nonnegative `x`. Both hold for
`beta_0`. No minimality or continuity property of `beta*` is used.

The paper's displayed certificate was independently expanded exactly:

\[
P_{\beta_0}(x)=\beta_0
\left(x^2-\frac{747}{1240}x-\frac{211}{1000}\right)^2
+\frac{708654527125x^2-1203303717450x+510806838853}
{6119661950000}.
\]

The second quadratic has positive leading coefficient and discriminant

```text
-2478929365735048000,
```

so it is positive on all real `x`. Hence `P_beta0(x) > 0` for all real `x`.

The structural induction also survives the replacement. With
`Delta = Delta(H)`, `sigma = sigma_G(H)`, and the paper's induced subgraph
`F = H[B]`, its counting gives

\[
|E(H)|\le \Delta(\sigma-\Delta)
+\frac{\Delta^2\beta_0(\sigma-\Delta)^2}
{\Delta^2+\beta_0(\sigma-\Delta)^2}.
\]

The key inherited-clique claim is valid: a length-2 path in `L(G)` between two
edges uses a middle edge joining endpoints of those two edges, so it remains in
the graph induced by their endpoints. Also, for each edge of `F`, all `Delta`
neighbors in `A` are removed from the endpoint degree sum, giving
`sigma_{G[B]}(F) <= sigma - Delta`. The source explicitly handles the
`h_x+f_x=0` case in its weighted inequality.

Setting `t = Delta/sigma` gives `0 < t < 1`; the strict upper inequality follows
from `sigma >= Delta+1` along an edge at a maximum-`H`-degree vertex. Exact
symbolic simplification confirms

\[
\beta_0-\left[t(1-t)+
\frac{\beta_0t^2(1-t)^2}{t^2+\beta_0(1-t)^2}\right]
=\frac{(1-t)^4P_{\beta_0}(t/(1-t))}
{t^2+\beta_0(1-t)^2}\ge0.
\]

Thus KMP Theorem 1.6 has a complete fixed-constant repair.

## 4. Faron--Postle dependency

Faron--Postle Theorem 1.9 has the exact quantifiers needed here. For a graph
`G`, a subgraph `H` whose edges form a clique in `L(G)^2`, and
`a in [1/4,1/3]`, assume that every bipartite `H'` contained in `H` with fewer
edges satisfies

\[
|E(H')|\le a\,\sigma_{G[V(H')]}(H')^2.
\]

Then

\[
|E(H)|\le\frac{1+a}{4}\sigma_G(H)^2.
\]

Apply repaired KMP Theorem 1.6 to `H'` with ambient graph `G[V(H')]`.
The inherited-clique observation above supplies precisely the hypothesis, and
`a = beta_0` is in the permitted interval. Therefore

\[
|E(H)|\le\frac{2607}{7948}\sigma_G(H)^2.
\]

For a clique edge-set in `G`, `sigma_G(H) <= 2 Delta(G)`, yielding KMP
Corollary 1.7. This conversion is rigorous modulo the named published
Faron--Postle theorem. It was not formally verified here. The Faron--Postle
arXiv source has an evident missing square on `sigma` in one Case 1 display;
the immediately preceding squared expression equals the theorem's stated
`(1+a)sigma^2/4`, so this is editorial and not load-bearing.

## 5. Delta = 4 rounding

For `Delta(G) <= 4`, Corollary 1.7 gives

\[
\omega(L(G)^2)\le16\frac{2607}{1987}
=\frac{41712}{1987}=21-\frac{15}{1987}<21.
\]

Clique number is an integer, hence `omega(L(G)^2) <= 20`. There is no off-by-one
or ceiling issue.

## 6. Equality construction

Let the five parts `P_0,...,P_4` each have two vertices. Make every part
independent and put all four edges between `P_i` and `P_{i+1}` modulo 5.
Then:

- there are 10 vertices and `5 * 2^2 = 20` edges;
- every vertex has two neighbors in each adjacent part, so the graph is
  4-regular;
- two edges from the same or adjacent edge-block of the base `C5` have a
  common incident edge unless already incident;
- two edges from nonadjacent edge-blocks have a common incident edge in the
  intervening complete bipartite block.

Thus every pair of its 20 edges has line-graph distance at most 2 and
`L(C5^(2))^2 = K20`. An independent NetworkX construction found 60 pairs at
distance 1 and 130 at distance 2, all 190 unordered pairs. Therefore both the
clique number and chromatic number of this particular line-graph square are 20.

This proves `Omega_4 >= 20`, and the rounded KMP bound proves equality.

## 7. Coloring boundary

The construction gives `X_4 >= 20`. Huang--Santana--Yu Theorem 2 proves that
graphs of maximum degree at most four have strong chromatic index at most 21
(their theorem is actually stated in a broader loopless multigraph setting).
Hence `20 <= X_4 <= 21`.

Nothing in KMP or the clique calculation rules out `X_4 = 21`. This is the
exact reason Problem 149 remains open at `Delta = 4`.

## 8. Local overlap and reproducibility

The frozen current snapshots of the two site source schemas contain neither a
Problem 149 article/ledger row nor the coefficients `2607/1987` and
`620/1987`. They do contain ledger Problem 934, which cites the same KMP paper.
That entry explicitly treats Section 3: `h_3`, Odd/Witt constructions,
projective-plane lifts, and the `L(G)^3` degree-diameter framework. It does not
treat KMP Section 2, the strong-clique coefficient, Delta = 4 rounding, or the
Problem 149 scope. The same-paper overlap is real and must remain disclosed;
the mathematical result audited here is distinct.

One bundle-infrastructure issue is recorded as `GAP` but does not affect the
mathematics. `audit_local_absence.py` reads live files outside the bundle's
manifest. Its frozen stdout reports 585 referenced problem numbers, while a
rerun during this audit reported 586 after unrelated site edits. Both runs kept
Problem 149 and the coefficient absent. The original `run_all.sh` is therefore
not a fully frozen reproduction of that count. This independent audit stores
compressed snapshots of both site files and hashes them in its own manifest.

## 9. Trust boundary

- Exact rational algebra, rounding, graph degrees, edge counts, all line-graph
  distances, source hashes, and local-snapshot absence were independently
  recomputed.
- KMP Lemma 2.2 was checked line by line under the fixed-constant repair.
- Faron--Postle Theorem 1.9 and Huang--Santana--Yu Theorem 2 remain named
  literature dependencies, not formalized proofs in this audit.
- KMP is an unrefereed v1 preprint with a disclosed source typo.
- The targeted current search found no newer general `Delta = 4` coloring
  theorem improving 21, but no claim of exhaustive literature completeness is
  made.

Final classification:

```text
PASS (scoped partial): Omega_4 = 20 for finite simple graphs, as a
literature-derived corollary with a disclosed fixed-beta repair.

GAP/OPEN (full Problem 149): only 20 <= X_4 <= 21 is justified.
```
