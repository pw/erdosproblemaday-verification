# Problem 617: an exact Ramsey edge frontier

Frozen: 2026-08-11 UTC

## Scope and provenance

This bundle proves the following exact auxiliary theorem for every integer
`r >= 2`.  Define

\[
  m_r=\min\{e(G): |V(G)|=r^2+1,\ \omega(G)\leq r,\ \alpha(G)\leq r\}.
\]

\[
  \boxed{m_r=\frac{r^3-r^2+4r-2}{2}}.
\]

In particular, `m_5=59` for the 26-vertex frontier.

Erdos Problem 617 itself is stated for `r >= 3`.  The case `r=2` is included
only to close the quantifier in this auxiliary theorem; there, `J` and its
complement are both 5-cycles, and the corresponding two-color partition is
why the original coloring statement is false at `r=2`.

This is relevant to, but does **not** solve, Erdos Problem 617.  In any
`r`-coloring that would witness failure of the problem, each color graph has
clique number and independence number at most `r`, so every color class has at
least `m_r` edges.  Compared with the total number of edges, this leaves

\[
  \binom{r^2+1}{2}-r m_r=\frac{r(r-1)(r-2)}2
\]

edges of slack.  At `r=5`, the class lower bounds total 295 out of 325 edges,
leaving 30.  The theorem neither proves that the color graphs are compatible
nor constructs their required edge partition.

Problem 617 was not genuinely untouched locally.  The site source records a
2026-05-26 off-site partial attempt concerning two different computational
obstructions (nonexistence of an affine `K_25 -> K_26` extension and
non-rigidity).  The exact general edge frontier above is the new scope of this bundle.
No site source, ledger, or deployment file was edited.

## Exact proof

### Lower bound

Fix `r >= 2`.  Let `G` be a graph on `n=r^2+1` vertices with
`omega(G) <= r` and `alpha(G) <= r`, and put `H = complement(G)`.

1. Since `alpha(G) <= r`, the graph `H` is `K_(r+1)`-free.
2. Since `alpha(H) = omega(G) <= r`, every proper coloring of `H` has at
   least

   \[
     \left\lceil\frac{r^2+1}{\alpha(H)}\right\rceil
     \geq \left\lceil\frac{r^2+1}{r}\right\rceil=r+1
   \]

   colors.  Thus `chi(H) > r`, so `H` is not `r`-partite.
3. Kang and Pikhurko define

   \[
     \mathcal G_{n,r}=\{F:v(F)=n,\ K_{r+1}\not\subseteq F,\ \chi(F)>r\}
   \]

   and `p_r(n) = max { e(F) : F in G_{n,r} }`.  Their Theorem 1, on journal
   page 13 (PDF page 2), has the following complete quantifiers and branches:
   for `n >= r+3` and `r >= 2`,

   \[
   p_r(n)=
   \begin{cases}
     t_r(n)-2,&r>(n-1)/2,\\
     t_r(n)-\lfloor n/r\rfloor+1,&r\leq(n-1)/2,
   \end{cases}
   \]

   where `t_r(n)` is the number of edges in the balanced `r`-partite Turan
   graph.

   For `n=r^2+1`, the hypotheses hold because
   `n-(r+3)=(r-2)(r+1) >= 0`, and the second branch applies because
   `r <= (n-1)/2 = r^2/2`.
4. The balanced part sizes for `T_r(r^2+1)` are one part of size `r+1` and
   `r-1` parts of size `r`.  Also `floor((r^2+1)/r)=r`.  Therefore

   \[
   e(H)\leq p_r(r^2+1)
   =\binom{r^2+1}{2}
    -\binom{r+1}{2}-(r-1)\binom r2-r+1.
   \]
5. Complementation now gives

   \[
     e(G)\geq
     \binom{r+1}{2}+(r-1)\binom r2+r-1
     =\frac{r^3-r^2+4r-2}{2}.
   \]

### Upper bound

Take disjoint sets `X,Y` with `|X|=r`, `|Y|=r+1`, and choose distinct
`y_1,y_2` in `Y`.  Starting from `K_(r,r+1)` with bipartition `(X,Y)`, add
the edge `y_1 y_2`.  For each `x in X`, delete exactly one of `x y_1` and
`x y_2`, arranging that both kinds of deletion occur.  This is possible
because `r >= 2`; call the resulting graph `J`.

The graph `J` has

\[
  e(J)=r(r+1)+1-r=r^2+1.
\]

It is triangle-free.  Indeed, its only edge within either part is `y_1 y_2`,
so a triangle would have to use that edge and some `x in X`; but `x` is
missing one of its two required incident edges.

Also `alpha(J)=r`.  The set `X` gives the lower bound.  For the upper bound,
an independent set containing any vertex of `Y - {y_1,y_2}` contains no
vertex of `X` and has size at most `r`, since `y_1 y_2` is an edge.  Every
remaining independent set lies in `X union {y_1,y_2}`.  It contains at most
one `y_i`; if it contains one, that `y_i` has a neighbor in `X` because both
deletion types occur, so at most `r-1` vertices of `X` can join it.  Thus its
size is again at most `r`.  Since `J` has edges and no triangle,
`omega(J)=2`.

Now let

\[
  G=(r-2)K_r\ \mathbin{\dot\cup}\ \overline J,
\]

where zero copies of `K_r` are used when `r=2`.  It has

\[
  (r-2)r+(2r+1)=r^2+1
\]

vertices, and

\[
\begin{aligned}
e(G)
  &=(r-2)\binom r2+\binom{2r+1}{2}-(r^2+1)\\
  &=\frac{r^3-r^2+4r-2}{2}.
\end{aligned}
\]

For disjoint unions, clique number is the maximum across components and
independence number is the sum.  Hence

\[
\alpha(G)=(r-2)+\omega(J)=r.
\]

For `r >= 3`, the clique number is the maximum of `r` from a `K_r` component
and `alpha(J)=r` from `complement(J)`.  For `r=2`, there is no `K_r`
component, but the sole component `complement(J)` has clique number
`alpha(J)=2`.  Thus `omega(G)=r` in every case.

This proves that the lower bound is attained for every `r >= 2`.

### Explicit `r=5` instance

For a fully finite check at the next open case of Problem 617, let `J` be the
graph on vertices `0,...,10` with the following 26 edges:

```text
01 12 13 14 05 06
27 37 47 57 67
28 38 48 58 68
29 39 49 59 69
2A 3A 4A 5A 6A
```

Here `A` denotes vertex 10.  This is the general construction with
`X={2,3,4,5,6}`, `Y={0,1,7,8,9,10}`, and `{y_1,y_2}={0,1}`.  Direct
exhaustive checking also shows that `J` has no triangle and no independent set
of size 6, so `omega(J)=2` and `alpha(J)=5`.

Construct `G` as the disjoint union of three copies of `K_5` and
`complement(J)`.  Then

\[
e(G)=3\binom52+\left(\binom{11}{2}-26\right)=30+29=59.
\]

For a disjoint union, clique number is the maximum of the component clique
numbers and independence number is the sum of the component independence
numbers.  Consequently

\[
\omega(G)=\max(5,\alpha(J))\leq5,
\qquad
\alpha(G)=1+1+1+\omega(J)\leq5.
\]

Thus `G` is admissible and has 59 edges, independently checking the `r=5`
instance of the general construction.

## Reproduction

All checkers use only the Python standard library.  The two `r=5` checkers are
intentionally different implementations.

```sh
python3 verify_e6626.py
python3 verify_e6626_independent.py
python3 verify_general.py
sha256sum -c SHA256SUMS
```

`verify_e6626.py` starts from the explicit edge list and exhausts all triples,
all 6-subsets of the 11-vertex graph, and all 6-subsets of the constructed
26-vertex graph.  `verify_e6626_independent.py` starts from the graph6 string,
decodes it independently into bitsets, and computes exact clique and
independence numbers with a branch-and-bound recurrence.

`verify_general.py` constructs the whole family directly, checks its defining
adjacency pattern for `2 <= r <= 50`, independently exhausts the forbidden
subsets for small parameters, and tests the closed formulas through
`r=10000`.  These finite ranges are regression tests; the all-`r` completeness
comes from the preceding case proof, not extrapolation from computation.

The checkers verify the finite witness and all arithmetic.  They do not
machine-prove the published Kang--Pikhurko theorem; the archived paper and
precise theorem locator are therefore part of the proof dependency.

## Sources

- M. Kang and O. Pikhurko, *Maximum K_(r+1)-free graphs which are not
  r-partite*, Matematychni Studii 24 (2005), 12-20,
  DOI `10.30970/ms.24.1.12-20`.  Theorem 1 is on journal page 13, PDF page 2.
  Official landing page:
  <https://matstud.org.ua/texts/2005/24_1/24_1_012_020.html>
- The graph `J` was selected from Brendan McKay's complete Ramsey `(3,6)`
  graph data for 11 vertices.  That dataset is provenance only; the explicit
  witness is checked from scratch here:
  <https://users.cecs.anu.edu.au/~bdm/data/ramsey.html>
- Problem 617: <https://www.erdosproblems.com/617>
