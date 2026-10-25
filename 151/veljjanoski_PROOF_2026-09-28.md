# Erdős #151 for all graphs on at most 39 vertices

**Theorem.** Every graph $G$ on $n \le 39$ vertices satisfies $\tau(G) \le n - H(n)$.

Here $\tau(G)$ is the least number of vertices meeting every maximal clique of $G$ with at least two vertices, and
$H(n) = \max\{k : R(3,k) \le n\}$ is the largest $k$ such that every triangle-free graph on $n$ vertices has an independent
set of size $k$. This is a problem of Erdős and Gallai (P. Erdős, 1988, p. 82), Problem 1 in P. Erdős, T. Gallai and
Zs. Tuza, *Covering the cliques of a graph with vertices*, Discrete Math. 108 (1992) 279–289, and
https://www.erdosproblems.com/151.

**Credit.** The reduction used here was posted on 25 Sep 2026 by GitHub user AlyciaBHZ in
[the-omega-institute/trureturing#9934](https://github.com/the-omega-institute/trureturing/issues/9934), an AI-assisted
research log. It contains Lemmas 1 and 2, Corollaries 1 and 2, and the arguments of Cases A and B below (the issue argues
Case B differently): every minimum counterexample has $n = R(3,k)$ and $R(3,k) - R(3,k-1) \le k - 3$. Citing a
clique-colouring theorem of Liang, Shan and Kang (Graphs Combin. 32 (2016) 1473–1488), the issue strengthens this to
$\le k - 4$. It states the consequences $n \le 27$ and $n = 28$; with $R(3,9) = 36$ and $R(3,10) \ge 40$ its conditions in
fact already give every $n \le 39$, although it does not say so. The new part here is **Case C**, an elementary proof of
the case where every link has $\beta \le 2$. It replaces the cited theorem, so the theorem follows from this note and the
Ramsey values alone; it also gives the Remark at the end.

AI-usage disclosure: Claude (Anthropic) was used as assistant. The argument was checked with AI referee passes and
computer sanity checks (every lemma on all graphs with at most 7 vertices; the Case C construction, implemented literally,
on thousands of random graphs); it has not been checked by a human referee. The computer verification for $n \le 22$ in [README.md](README.md) is consistent with this and is no longer needed for it.

## Notation

"Clique" means a maximal clique with at least 2 vertices. A vertex set $U$ is *free* if it contains no clique, and
$\beta(G)$ is the largest size of a free set. The complement of a free set meets every clique, so
$\beta(G) = n - \tau(G)$ and the conjecture reads $\beta(G) \ge H(n)$. For a vertex $v$, $P_v$ is the graph induced on the
neighbourhood $N(v)$ with its isolated vertices removed. The graph with no vertices has $\beta = 0$. $\Delta$ is the maximum degree.

## Basic facts

- **(F1)** $\alpha(G) \le \beta(G)$: an independent set contains no edge, so no clique.
- **(F2)** If $G$ is triangle-free, $\beta(G) \ge \alpha(G) \ge H(n)$, by the definition of $R(3,k)$.
- **(F3)** $\Delta(G) \le \beta(G)$: $N(v)$ is free, because a clique inside $N(v)$ extends by $v$ and so is not maximal.
- **(F4)** Every graph with at least one vertex has $\beta \ge 1$ (one vertex contains no clique). Hence a graph with $\beta = 0$ has no
  vertices, and $\beta(P_v) = 0$ means $N(v)$ is independent.

**Lemma 1 (vertex deletion).** $\beta(G - v) \le \beta(G)$.

*Proof.* Let $U$ be free in $G - v$ and suppose $U$ contains a clique $C$ of $G$. Then $v \notin C$, and no vertex of
$G - v$ is adjacent to all of $C$, so $C$ is a clique of $G - v$ inside $U$: a contradiction. So $U$ is free in $G$. $\square$

**Lemma 2 (local bound).** Let $D \subseteq N(v)$ meet every nonempty maximal clique of $G[N(v)]$, where isolated vertices of
$G[N(v)]$ count as one-vertex cliques. Then $\beta(G) \ge 1 + \beta(G - v - D)$. The smallest such $D$ has size
$d(v) - \beta(P_v)$.

*Proof.* Let $U'$ be free in $G' = G - v - D$ and $U = U' \cup \{v\}$. Suppose $U$ contains a clique $C$ of $G$.
If $v \notin C$, then $C \subseteq U'$ and $C$ is a clique of $G'$ (a vertex of $G'$ adjacent to all of $C$ would extend it
in $G$), a contradiction. If $v \in C$, then $C - v$ is nonempty, lies in $U'$, and is a maximal clique of $G[N(v)]$
(a vertex of $N(v)$ adjacent to all of $C - v$ would extend $C$), so $D$ meets it, contradicting $U' \cap D = \emptyset$.
For the size: $D$ must contain every isolated vertex of $G[N(v)]$, and the remaining condition is exactly that $D$ meets
every clique of $P_v$; the least such set has size $|V(P_v)| - \beta(P_v)$. $\square$

## Minimum counterexample

Suppose the theorem fails and let $G$ be a counterexample with the fewest vertices: $\beta(G) \le k - 1$ where
$k = H(n)$. Put $g = R(3,k) - R(3,k-1)$ (with $R(3,0) = 0$, $R(3,1) = 1$).

**Corollary 1.** $n = R(3,k)$. *Proof.* If $n - 1 \ge R(3,k)$ then $H(n-1) = k$, and by Lemma 1 $G - v$ is a smaller
counterexample. $\square$

**Corollary 2.** For every vertex $v$: $\beta(P_v) \le d(v) - g \le k - 1 - g$.

*Proof.* Take $D$ of size $d(v) - \beta(P_v)$ in Lemma 2. The graph $G' = G - v - D$ has
$n - 1 - d(v) + \beta(P_v)$ vertices. If this is at least $R(3,k-1)$, then $G'$ is not a counterexample (it is smaller),
so $\beta(G') \ge H(|G'|) \ge k - 1$ and Lemma 2 gives $\beta(G) \ge k$, a contradiction. Hence
$n - 1 - d(v) + \beta(P_v) \le R(3,k-1) - 1$, which is the first inequality. The second is $d(v) \le \beta(G) \le k - 1$
by (F3). $\square$

Write $B = k - 1 - g$. By Corollary 2 every link satisfies $\beta(P_v) \le B$, and by (F1) and (F3) applied to $P_v$
also $\alpha(P_v) \le B$ and $\Delta(P_v) \le B$.

## The cases $B \le 2$

**Case $B < 0$.** Impossible, since $\beta(P_v) \ge 0$. (Also $k = 1$ is impossible outright: $\beta(G) \ge 1$ by (F4).)

**Case A: $B = 0$.** By (F4) every $N(v)$ is independent, so $G$ is triangle-free, and (F2) gives $\beta(G) \ge k$:
a contradiction.

**Case B: $B = 1$.** Each $P_v$ has maximum degree at most 1 and no isolated vertices, so it is a matching; a matching
with $m$ edges has $\beta = m$ (one endpoint of each edge), so $P_v$ is empty or a single edge. Hence every vertex lies in
at most one triangle: the triangles are vertex-disjoint and $G$ has no $K_4$. Let $G^*$ be $G$ with two edges deleted from
every triangle. $G^*$ is triangle-free, and it keeps an edge of every clique of $G$ (the cliques are the triangles and the
edges in no triangle). So every independent set of $G^*$ is free in $G$, and $\beta(G) \ge \alpha(G^*) \ge H(n) = k$ by
(F2): a contradiction.

**Case C: $B = 2$.**
- $\Delta(P_v) \le 2$ for every $v$, so the edge $uv$ lies in $|N(u) \cap N(v)| \le 2$ triangles (this is the degree of $u$
  in $P_v$, or $0$). Hence $G$ has no $K_5$. The rest of Case C uses only this property.
- If $K$ is a $K_4$ and $v \in K$, then $K - v$ is a triangle in $P_v$ whose vertices have degree 2 there, so it is a
  component of $P_v$. Hence every edge of $K$ lies only in the two triangles inside $K$; in particular two $K_4$'s share
  no edge, and no triangle outside $K$ shares an edge with $K$.
- The cliques of $G$ are therefore: the $K_4$'s, the triangles not inside a $K_4$ (call them *lone triangles*), and the
  edges in no triangle.
- Let $M$ be the multigraph whose nodes are the lone triangles plus one extra node $z_0$. Every edge $e$ of $G$ lying in a
  lone triangle gives one edge of $M$: it joins the two lone triangles containing $e$ if there are two, and joins the
  lone triangle to $z_0$ if there is only one. Every lone triangle has degree exactly 3 in $M$.
- **Claim.** The edges of $M$ can be coloured red and blue so that every lone triangle has edges of both colours. If
  there is no lone triangle this is empty. Otherwise delete $z_0$ if it is isolated, and add a new node $z$ joined to
  every node of odd degree. All degrees become even (the number of odd-degree nodes is even), and the graph is connected:
  every lone triangle has degree 3, hence is joined to $z$, and $z_0$ (if kept) is adjacent to a lone triangle. Colour
  the edges of an Euler circuit starting at $z$ alternately red and blue. Every time the circuit passes through a node
  $x \ne z$ it uses two consecutive edges, of different colours. A lone triangle has degree 4 in this augmented graph
  and is passed twice; only one of its edges goes to $z$, so one of the two passes uses two edges of $M$, one red and
  one blue.
- Let $G^*$ be the spanning subgraph of $G$ (all $n$ vertices) whose edges are the edges of $G$ in no triangle, a 4-cycle
  inside each $K_4$, and the edges of $G$ whose $M$-edge is red.
  $G^*$ is triangle-free: a triangle of $G^*$ is a triangle of $G$; if it lies inside a $K_4$ it would need three edges of
  that $K_4$ forming a triangle, but $G^*$ contains only a 4-cycle of it (edges of a $K_4$ are in no other $K_4$ and are not
  edges of $M$); otherwise it is a lone triangle, which has a blue edge, not in $G^*$.
- $G^*$ contains an edge of every clique of $G$. So $\beta(G) \ge \alpha(G^*) \ge H(n) = k$: a contradiction.

**Conclusion.** No minimum counterexample has $R(3,k) - R(3,k-1) \ge k - 3$ (that is, $B \le 2$).

## Ramsey values

$R(3,k)$ for $k = 1, \dots, 9$ is $1, 3, 6, 9, 14, 18, 23, 28, 36$, and $40 \le R(3,10) \le 41$ (S. Radziszowski, *Small Ramsey
Numbers*, Electron. J. Combin., Dynamic Survey DS1, revision 18, 2026; the upper bound $41$ is due to V. Angeltveit).
Only $R(3,10) \ge 40$ is used.

| $k$ | $n = R(3,k)$ | $R(3,k-1)$ | $g$ | $B = k - 1 - g$ | case |
|---|---|---|---|---|---|
| 2 | 3 | 1 | 2 | $-1$ | impossible |
| 3 | 6 | 3 | 3 | $-1$ | impossible |
| 4 | 9 | 6 | 3 | $0$ | A |
| 5 | 14 | 9 | 5 | $-1$ | impossible |
| 6 | 18 | 14 | 4 | $1$ | B |
| 7 | 23 | 18 | 5 | $1$ | B |
| 8 | 28 | 23 | 5 | $2$ | C |
| 9 | 36 | 28 | 8 | $0$ | A |

A smallest counterexample on at most 39 vertices would have $k = H(n) \le 9$, because $R(3,10) \ge 40$. Every such $k$ is
excluded, which proves the theorem.

## Where it stops

At $k = 10$, $n = R(3,10) \in \{40, 41\}$, $g \in \{4, 5\}$ and $B \in \{5, 4\}$. Links may then contain $K_4$'s and
edges may lie in many triangles, and Case C does not apply as it stands.

## Remark

Case C does not use minimality: it only uses that every edge lies in at most two triangles. So every graph in which
each edge lies in at most two triangles satisfies $\tau(G) \le n - H(n)$, for every $n$ (with $H(n)$ as defined, whether
or not its value is known). No novelty is claimed for this observation.
