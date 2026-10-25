# Problem 708: the new eleven-edge two- and three-defect kernels

Date: 2026-08-11 UTC

Status: finite generic-kernel classification and candidate repair proof.  This
is a component of, not a complete proof of, `c_11=2`.

## 1. Structural reduction

For an edge set `S` in a simple bipartite graph, write

\[
                         d(S)=|S|-|N(S)|.
\]

An inclusion-minimal `q`-defect kernel has minimum degree at least two.  If
it has eleven edges, it has `11-q` active vertices.

Both active bipartition classes have size at least two.  For `q=2`, the
bipartition sizes of the nine vertices cannot be `2+7` or `3+6`, since
minimum degree two on the larger side would require at least 14 or 12 edges.
Thus every new two-defect kernel is `4 x 5`.

For `q=3`, the eight vertices cannot split as `2+6`, for the same reason.
The new three-defect kernels are therefore `3 x 5` or `4 x 4`.

For `q=4`, seven vertices and eleven edges force the already treated
`K_(3,4)-e`.  A defect at least five is impossible, because a bipartite
graph on at most six vertices has at most nine edges.

## 2. Eleven-edge/two-defect certificates

Up to row and column permutations, there are eleven inclusion-minimal
eleven-edge/two-defect `4 x 5` graphs.  Each row below gives the adjacency
matrix followed by two five-edge blocks `P,Q`.

```text
11111/11000/10100/00011  P=00,01,02,10,11  Q=00,03,04,33,34
11110/11100/10001/00011  P=00,01,02,10,11  Q=00,03,10,20,24
11110/11100/00011/00011  P=00,01,02,10,11  Q=03,23,24,33,34
11110/11001/10100/00011  P=00,01,02,10,11  Q=00,03,10,14,33
11110/11001/10001/00110  P=00,01,02,03,10  Q=00,10,14,20,24
11110/11001/00110/00101  P=00,01,02,10,11  Q=02,03,14,22,23
11110/11001/00101/00011  P=00,01,10,11,14  Q=02,03,14,22,24
11100/11100/10011/00011  P=00,01,02,10,11  Q=00,10,20,23,24
11100/11010/10101/00011  P=00,01,02,10,11  Q=00,10,13,20,24
11100/11010/10001/00111  P=00,01,02,10,11  Q=00,10,13,20,24
11100/11010/00111/00101  P=00,01,02,10,11  Q=02,13,22,23,24
```

For every endpoint-induced prime-power level `K`, direct inspection gives

\[
        \#\{B\in\{P,Q\}:B\subseteq E(K)\}
             \ge \max(0,|E(K)|-|V(K)|).                            \tag{1}
\]

The standard layer assignment therefore produces repair factors `r,s` with

\[
 \prod_{e\in E(G)}a_e\mid\left(\prod_{v\in V(G)}v\right)rs,
 \qquad r\mid a_e\ (e\in P),\quad s\mid a_e\ (e\in Q).            \tag{2}
\]

In particular `r,s<=M/5`.  Each has at least nine interval multiples.  If
one had no multiple outside the nine kernel vertices, all nine vertices
would be divisible by it; exact differences would make it divide all eleven
labels, giving at least 21 multiples.  Thus each has an outside multiple.

We use the following ten-point progression lemma.

**Lemma.**  If `d,e<=M/5`, each has at least nine multiples in an open
interval of length `2M`, and

\[
                         |Z(d)\cup Z(e)|\le10,                      \tag{3}
\]

then `d=e`.

Indeed, (3) implies `d,e>=2M/11`.  If the reduced ratio of the larger to the
smaller is `v/u>1`, then `v/u<=11/10`, so `u>=10,v>=11`.  Their least common
multiple is at least `11(2M/11)=2M`.  On the other hand their two sets, each
of size at least nine inside a ten-point union, have at least eight common
points, impossible in an open interval of length `2M`.

If the two outside-multiple sets failed Hall, (3) would hold.  The lemma
would give `r=s`.  Every displayed pair has union of at least six edges, so
the common factor divides at least six distinct labels and has at least
eleven multiples, contradicting (3).  Thus the two repair factors have
distinct multiples outside the nine vertices.  This completes every new
eleven-edge/two-defect kernel.

## 3. Eleven-edge/three-defect certificates

There are three `3 x 5` and eight `4 x 4` isomorphism classes.  The three
four-edge blocks following each matrix are `P,Q,R`.

```text
3x5
11111/11110/10001  P=00,01,10,11  Q=00,04,10,20  R=02,03,12,13
11111/11100/10011  P=00,01,10,11  Q=00,02,10,12  R=03,04,23,24
11110/11101/10011  P=00,01,10,11  Q=00,02,10,12  R=03,14,23,24

4x4
1111/1110/1100/1001  P=00,01,02,10  Q=00,01,11,20  R=00,03,30,33
1111/1110/1100/0011  P=00,01,02,10  Q=00,01,11,20  R=02,03,32,33
1111/1110/1001/1001  P=00,01,02,10  Q=00,03,20,23  R=00,03,30,33
1111/1110/1001/0101  P=00,01,02,10  Q=00,03,20,23  R=01,03,11,31
1110/1110/1101/1001  P=00,01,02,10  Q=00,01,11,20  R=20,23,30,33
1110/1110/1101/0011  P=00,01,02,10  Q=00,01,20,21  R=12,23,32,33
1110/1101/1100/1011  P=00,01,02,10  Q=00,01,20,21  R=10,13,30,33
1110/1101/1011/0110  P=00,01,02,10  Q=01,02,22,31  R=10,13,20,23
```

Every table row satisfies the three-block analogue of (1).  Every pair of
blocks has at least six edges in its union, and all three have at least nine.
The layer principle gives factors `r,s,t`, each dividing four labels.

Each factor has an outside multiple.  It has at least seven interval
multiples.  If they all lay among the eight kernel vertices, at least seven
vertices would be divisible by the factor.  Removing the possible eighth
vertex deletes at most five edges in a `3 x 5` graph and at most four in a
`4 x 4` graph.  Hence the factor divides at least six labels, which would
give at least eleven interval multiples, a contradiction.

For pairs of factors, an outside Hall deficit would put their full union in
at most nine points.  The published nine-point progression lemma makes them
equal; their six-edge support union then gives at least eleven multiples.

For all three factors, an outside Hall deficit puts the full union in at
most ten points.  We need one further progression observation.

**Lemma.**  If `d,e<=M/4`, each has at least seven interval multiples, and
\(|Z(d)\cup Z(e)|\le10\), then `d=e`.

The union bound gives `d,e>=2M/11`.  A distinct reduced ratio at most
`(M/4)/(2M/11)=11/8` has denominator at least three and numerator at least
four.  Thus the lcm is at least `4(2M/11)=8M/11`.  The two sets have at least
four common points, which span at least `24M/11>2M`, a contradiction.

Applying this lemma pairwise makes `r=s=t`.  The common factor divides at
least nine labels and therefore has at least seventeen multiples, again
contradicting the ten-point union.  Hall supplies three distinct outside
repair points.

## 4. Exhaustive status and remaining integration gap

The independent checker enumerates all labelled graphs, not just the table:

```text
q=2, 4x5: 13,560 labelled kernels, 11 classes
q=3, 3x5:    390 labelled kernels,  3 classes
q=3, 4x4:  2,304 labelled kernels,  8 classes
```

It tests inclusion-minimality through every proper row/column-induced
subgraph, reconstructs the isomorphism classes, and verifies every
prime-power level and support-overlap condition.

This settles the genuinely new full eleven-edge kernels in the generic
exact-difference case.  The joint treatment of inherited smaller cores and
the aligned ten-label-away-from-the-midpoint construction are separate; they
are supplied in `erdos708_c11_candidate.md` and checked by
`erdos708_c11_full_audit.py`.
