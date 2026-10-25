# Erdős 813: every order-18 candidate has maximum degree at least 7

Let \(G\) be an 18-vertex graph satisfying

\[
\omega(G)\le 4,
\qquad
\text{every seven vertices of }G\text{ contain a triangle}.
\tag{1}
\]

Equivalently, \(G\) is \(K_5\)-free and has no triangle-free seven-set.

## Proposition

Every graph satisfying (1) has \(\Delta(G)\ge 7\).

## Proof

Suppose for a contradiction that \(\Delta(G)\le 6\).

First, \(\chi(G)\ge 6\).  Indeed, if \(G\) had a proper coloring with at
most five color classes, pad the coloring with empty classes if necessary.
The two largest of the resulting five classes would contain at least

\[
\left\lceil\frac{2\cdot18}{5}\right\rceil=8
\]

vertices: their total is at least twice the average class size.  Their
union is bipartite, hence triangle-free, and any seven of its vertices
contradict (1).

On the other hand, \(\chi(G)\le 6\).  Apply Brooks' theorem separately to
each connected component.  A component which is neither complete nor an
odd cycle has chromatic number at most its maximum degree, and therefore at
most 6.  A complete component has order at most 4 because \(G\) is
\(K_5\)-free, so it is at most 4-colorable.  An odd-cycle component is
3-colorable.  Coloring all components with a common palette of six colors
gives \(\chi(G)\le6\), including when \(G\) is disconnected.

Thus \(\chi(G)=6\).  Fix a proper six-coloring with color classes
\(C_1,\ldots,C_6\), and write \(c_i=|C_i|\).  For every distinct \(i,j\),
the union \(C_i\cup C_j\) is bipartite and therefore triangle-free.  By
(1),

\[
c_i+c_j\le6. \tag{2}
\]

There are fifteen inequalities in (2).  Their left sides sum to

\[
\sum_{i<j}(c_i+c_j)=5\sum_i c_i=5\cdot18=90,
\]

while their right sides sum to \(15\cdot6=90\).  Consequently equality
holds in every instance of (2).  All pair sums are six, so all \(c_i\) are
equal; hence

\[
|C_1|=\cdots=|C_6|=3. \tag{3}
\]

Choose a vertex \(z\in C_1\).  For each pair \(2\le i<j\le6\), consider
the seven-set

\[
S_{ij}=\{z\}\cup C_i\cup C_j.
\]

It contains a triangle by (1).  Because each color class is independent
and \(S_{ij}\) uses only two classes besides \(z\), every such triangle must
have the form \(zxy\), where \(x\in C_i\), \(y\in C_j\), and all three of
\(zx,zy,xy\) are edges.  It follows that:

1. \(z\) has a neighbor in each of \(C_2,\ldots,C_6\); and
2. for every pair of those five classes, some neighbor of \(z\) in one is
   adjacent to some neighbor of \(z\) in the other.

Since \(\deg(z)\le6\), its positive neighbor counts in these five classes
either are

\[
(1,1,1,1,1)
\]

or, up to order,

\[
(2,1,1,1,1).
\]

In the first case, the five unique class-neighbors of \(z\) are pairwise
adjacent by property 2, forming a forbidden \(K_5\).

In the second case, take the unique neighbor from each of the four singleton
classes.  Property 2 makes these four vertices pairwise adjacent, so they
form a \(K_4\); together with their common neighbor \(z\), they form a
forbidden \(K_5\).

Both cases contradict \(\omega(G)\le4\).  Therefore
\(\Delta(G)\ge7\). \(\square\)

## Consequence for the finite exhaustion

Combined with the independently audited bound \(\Delta(G)\le12\), an exact
maximum-degree split need only certify the six branches

\[
\Delta(G)=7,8,9,10,11,12.
\]

No degree-0 through degree-6 SAT branches are needed.
