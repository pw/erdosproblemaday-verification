# Problem 708: simultaneous placement for the `K_(3,4)-e` four-defect kernel

Date: 2026-08-11 UTC

Status: candidate proof of the previously open placement lemma.  This note
does **not** by itself prove `c_11=2`; the other kernels and the aligned case
are integrated separately in `erdos708_c11_candidate.md`.

## 1. Statement

Let

\[
                         I=(x,x+2M)
\]

and let `L_0,L_1,L_2` be distinct integer points in `(x,x+M]` and
`R_0,R_1,R_2,R_3` distinct integer points in `(x+M,x+2M)`.  Delete the edge
`(0,0)` from `K_(3,4)`.  Suppose that the eleven remaining differences

\[
                         a_{ij}=R_j-L_i
\]

are distinct positive integers at most `M`, and that `a_(ij)` divides both
of its endpoints.  Put

\[
 q_{ik,j}=\gcd(a_{ij},a_{kj})
\]

whenever both edges in column `j` exist, and put

\[
 F=\{L_0,L_1,L_2,R_0,R_1,R_2,R_3\},\qquad
 X_{ik,j}=q_{ik,j}\mathbb Z\cap I\setminus F.
\]

Write

\[
 \mathcal A=\{(01,j):j=1,2,3\},\quad
 \mathcal B=\{(02,j):j=1,2,3\},\quad
 \mathcal C=\{(12,j):j=0,1,2,3\}.
\]

**Placement lemma.**  There are `a,b in {1,2,3}` and distinct
`c,d in {0,1,2,3}` such that

\[
                       \neg(a=b\text{ and }a\in\{c,d\}),            \tag{1}
\]

and the four sets

\[
                  X_{01,a},X_{02,b},X_{12,c},X_{12,d}               \tag{2}
\]

have a system of distinct representatives.

The proof deliberately does not choose a fixed pair of `12` columns.  A
literal kernel with `M=70`, `x=805` has `q_(12,0)=35` and
`X_(12,0)=empty`, so no fixed choice involving column zero can work.

## 2. Multiple counts

For a positive integer `q`, write \(Z(q)=q\mathbb Z\cap I\).  The open-interval
count is

\[
                         |Z(q)|\ge \left\lceil {2M\over q}\right\rceil-1.
                                                                         \tag{3}
\]

If `q` divides `k` distinct positive labels at most `M`, their quotients by
`q` are `k` distinct positive integers.  Hence

\[
                         kq\le M,
       \qquad             |Z(q)|\ge 2k-1.                            \tag{4}
\]

Both endpoint conventions in (3) are sharp enough for everything below.

## 3. A confined-progression lemma

Fix one row pair `i,k`, let `h` be the third row, and set

\[
                         D=|L_i-L_k|.
\]

Consider some of the pair blocks `(ik,j)`.  Let \(T\subseteq I\setminus F\) have
size `t<=4`, and suppose that every outside multiple of each considered
block lies in `T`.

For such a block, write `q=q_(ik,j)`.  Since each edge label divides its
left endpoint, `q` divides `L_i` and `L_k`; consequently

\[
                         m={D\over q}\in\mathbb Z_{>0}.              \tag{5}
\]

The `m-1` internal `q`-multiples between `L_i` and `L_k` lie in the left
half.  At most one is the third row vertex `L_h`, and every other one is an
outside point and therefore belongs to `T`.  After affinely identifying the
row interval with `[0,1]`, put

\[
                         P_m=\{1/m,2/m,\ldots,(m-1)/m\}.
\]

Then

\[
                  m\le t+2,\qquad P_m\subseteq \{L_h\}\cup T,       \tag{6}
\]

where the second formula is understood in the original affine coordinates.

Let `n_m` count the considered blocks with the value in (5).  If `n_(m0)>0`,
then `D/m_0` divides `D/m` whenever `m|m_0`.  The corresponding two-edge
supports are disjoint between columns.  Thus `D/m_0` divides

\[
                         2C_{m_0}\quad\hbox{distinct labels},
       \qquad C_{m_0}=\sum_{m\mid m_0}n_m.                           \tag{7}
\]

All of its interval multiples lie in \(F\cup T\), so (4) gives

\[
                         4C_{m_0}-1\le 7+t.                         \tag{8}
\]

For `t<=3`, this says `C_(m0)<=2`.  For `t=4`, equality
`C_(m0)=3` in (8) would give at least eleven multiples inside the
eleven-point set \(F\cup T\).  Every kernel vertex would then be divisible
by `D/m_0`, so all eleven exact differences would be divisible by it.
Equation (4), now with `k=11`, would give at least 21 interval multiples, a
contradiction.  The same equality argument at `t=0` excludes
`C_(m0)=2`: seven multiples inside the seven-point set `F` make all eleven
labels divisible.  We have proved the uniform bound

\[
                         C_{m_0}\le2                                \tag{9}
\]

for every occurring `m_0` and every `0<=t<=4`, with the just-described
equality argument used at `t=0,4`.

The following consequences of (6) and (9) will be used repeatedly.

1. If `t=0`, at most one block can be confined to `T`.  Indeed, all `m` are
   in `{1,2}`; for two occurrences, either `m_0=2` captures both or both
   have `m=1`, contradicting the sharpened `t=0` case above.
2. If `t=1`, at most two blocks can be confined.  Three occurrences among
   `m=1,2,3` either give three indices dividing one occurring index, contrary
   to (9), or use both `m=2` and `m=3`.  In the latter case
   \(P_2\cup P_3=\{1/3,1/2,2/3\}\) has three points and cannot fit in
   \(\{L_h\}\cup T\), which has two.
3. If `t=2` or `t=3` and at least three blocks are confined, both `m=2`
   and `m=3` occur and
   \[
                       P_2\cup P_3=\{1/3,1/2,2/3\}
                            \subseteq\{L_h\}\cup T.                 \tag{10}
   \]
   For `t=2`, `m=4` either leaves all further occurrences among divisors of
   four, violating (9), or coexists with `m=3`, when
   \(|P_4\cup P_3|=5>3\); `m=5` is already too large.  For `t=3`, `m=5`
   fills the four available positions and cannot coexist with another
   nontrivial grid, while `m=1` is captured by five; `m=4` is disposed of
   in the same way using \(|P_4\cup P_3|=5>4\).  What remains is
   `m=1,2,3`, where (9) forces both two and three.  When `t=2`, both sides
   of (10) have three points, so
   \[
                       \{L_h\}\cup T=P_2\cup P_3.                  \tag{11}
   \]
   In particular, the third row lies strictly between the selected rows.
4. Suppose `t=4`, the third row lies outside the open interval between the
   selected rows, and at least three blocks are confined.  Then
   \[
                       P_2\cup P_3\subseteq T.                      \tag{12}
   \]
   Here `P_6` has five points and is impossible.  The four points of `P_5`
   fill `T`; every nontrivial grid with denominator at most six adds a new
   point, while occurrences with denominators one and five are bounded by
   (9).  If `m=4` occurs, all additional denominators except `1,2,4` make
   more than four grid points, while the occurrences with `1,2,4` are all
   captured by four and hence number at most two.  Thus only `1,2,3`
   remain, and (9) again forces both two and three.

This is the confined-progression lemma.

## 4. Two elementary geometry facts

For distinct real numbers `u,v`, let `P(u,v)` be the midpoint and the two
trisection points of their interval.

First, two different row pairs cannot both have their third row strictly
between their endpoints.  If the pairs share `u` and have other endpoints
`v,w`, the two assertions would say simultaneously
`|w-u|<|v-u|` and `|v-u|<|w-u|` when `v,w` lie on the same side of `u`;
on opposite sides neither assertion holds.

Second, for three distinct rows `u,v,w`,

\[
 |(P(u,v)\setminus\{w\})\cup(P(u,w)\setminus\{v\})|\ge4.           \tag{13}
\]

If `v,w` lie on opposite sides of `u`, the two open row intervals are
disjoint and the left side is six.  Otherwise choose `v` closer to `u` and
normalize `u=0,v=1,w=s>1`.  Put `S={1/3,1/2,2/3}`.  The two grids are
`S` and `sS`.  For `s>1`, \(S\cap sS\) has at most one point: the possible
ratios greater than one between members of `S` are `3/2,2,4/3`, each from a
unique ordered pair.  Removing the point `1` from `sS` deletes at most one
more point, so at least one point remains outside `S`.  This proves (13).

## 5. Rank bounds for all ten block occurrences

Make a bipartite graph `Gamma` whose left vertices are the ten block
occurrences in \(A\cup B\cup C\), whose right vertices are the integer
points of \(I\setminus F\), and where `(ik,j)` is adjacent to the points in
`X_(ik,j)`.  Let `r(S)` be the maximum matching size from a set `S` of left
vertices.  These are the ranks of the transversal matroid of `Gamma`.

We prove

\[
\begin{array}{c|c}
S&\text{lower bound}\\ \hline
\mathcal A,\mathcal B&1\\
\mathcal C&3\\
\mathcal A\cup\mathcal B&2\\
\mathcal A\cup\mathcal C,
\mathcal B\cup\mathcal C&4\\
\mathcal A\cup\mathcal B\cup\mathcal C&5.
\end{array}                                                         \tag{14}
\]

For any alleged smaller rank, Konig's theorem gives a vertex cover made of
`h` left block occurrences and a common set `T` of `t` outside points, with
`h+t` at most the alleged rank.  Every block occurrence not in the left part
of the cover is confined to `T`, so Section 3 applies separately to each row
pair.

For `A` or `B`, rank zero would leave all three blocks confined with `t=0`,
contrary to the first confinement bound.  For `A union B`, rank at most one
has two possibilities.  If `t=0`, deleting at most one block leaves more
than one confined block in at least one family.  If `t=1`, no block is
deleted and each three-block family exceeds the `t=1` capacity.  Thus the
first, second, and fourth entries of (14) hold.

Suppose `r(C)<=2`.  For `t=0` or `1`, after deleting at most `2-t` blocks,
respectively at least two or three `C` blocks remain, contradicting the
corresponding capacities.  If `t=2`, no block is deleted and all four `C`
blocks are confined.  By (10), only denominators `1,2,3` occur and both two
and three occur.  If their multiplicities are `n_1,n_2,n_3`, (9) gives

\[
                         n_1+n_2\le2,\qquad n_1+n_3\le2.
\]

Their sum is four, so `n_1=0` and `n_2=n_3=2`.  By (11), the third row
`L_0` is a midpoint or trisection point.  Let `m_*` be `2` or `3`
accordingly and put `q_*=|L_1-L_2|/m_*`.  This value occurs in two `C`
columns and divides all three row vertices and the corresponding two right
vertices.  Those five vertices induce at least five existing kernel edges
(a column zero contributes two rather than three), so `q_*` divides at
least five distinct labels.  It has at least nine interval multiples by
(4), all inside the nine-point set \(F\cup T\); hence every kernel vertex is
`q_*`-divisible.  All eleven labels are then divisible by `q_*`, giving at
least 21 multiples, a contradiction.  Therefore `r(C)>=3`.

Consider `A union C`; the proof for `B union C` is identical.  If its rank
were at most three, take `h+t<=3`.  At `t=0`, the two families require at
least `2+3` left deletions to respect the capacity one.  At `t=1`, they
require at least `1+2` deletions to respect capacity two.  Both exceed the
available `h`.  At `t=2`, at most one block is deleted.  If it is not a
`C` block, all four `C` blocks are confined, which was just shown
impossible.  If it is a `C` block, three blocks from each row pair remain;
by (11), each pair would have its third row between its endpoints, contrary
to the first geometry fact.  At `t=3`, no block is deleted.  Formula (10)
and (13) say that the common three-point set `T` would have to contain at
least four points.  Hence both mixed ranks are at least four.

Finally suppose the full ten-block graph had rank at most four, and take
`h+t<=4`.  At `t=0`, capacities one would require at least `2+2+3=7`
left deletions.  At `t=1`, capacities two require at least `1+1+2=4`,
again more than the available `h`.  At `t=2`, if no `C` block is deleted,
the impossible four-block `C` configuration remains.  If one `C` block is
deleted, at most one further deletion is available, so `C` and at least one
other family retain three confined blocks; if two `C` blocks are deleted,
both other families retain three.  In either case (11) gives two impossible
betweenness assertions.  At `t=3`, at most one block is deleted, so at least
two row-pair families retain three blocks; (10) and (13) require at least
four points in `T`.  At `t=4`, no block is deleted.  Order the three row
vertices.  The two adjacent row-pair families have their third row outside
their open intervals, so (12) puts three midpoint/trisection points from
each of two disjoint open intervals into the four-point set `T`, a final
contradiction.  Thus the full rank is at least five, completing (14).

## 6. Rado selection and removal of the forbidden pattern

Use Rado's independent-transversal theorem in the transversal matroid above
on five sets: one copy of `A`, one copy of `B`, and three copies of `C`.
Its rank conditions are precisely

\[
 r(A)\ge1,\ r(B)\ge1,\ r(C)\ge3,\ r(A\cup B)\ge2,
\]
\[
 r(A\cup C)\ge4,\ r(B\cup C)\ge4,\ r(A\cup B\cup C)\ge5,
\]

which are (14).  (For a subset containing fewer identical `C` copies, the
same union occurs and the required right side only decreases.)  We obtain
one `A` block, one `B` block, and three distinct `C` blocks which together
have five distinct outside representatives.

Let the first two selected columns be `a,b`.  If `a!=b`, discard any one of
the three `C` blocks.  If `a=b=j` and the selected `C` blocks include column
`j`, discard that block; if they do not, discard any selected `C` block.  In
either case at least two retained `C` columns differ from `j`.  The four
retained blocks satisfy (1).  A subset of an independent set
is independent, so their four outside-multiple sets have distinct
representatives.  This proves the placement lemma.

## 7. Connection to the four-defect valuation certificate

The separate finite layer certificate shows that the admissible four-tuples
are exactly

\[
 q_{01,a},q_{02,b},q_{12,c},q_{12,d},\qquad
 c\ne d,\quad\neg(a=b\text{ and }a\in\{c,d\}),
\]

and, if `R` is the gcd of their 45 four-factor products, then

\[
 \prod_{(i,j)\ne(0,0)}a_{ij}
       \mid L_0L_1L_2R_0R_1R_2R_3\,R.                              \tag{15}
\]

The tuple supplied above is admissible, so `R` divides its four-factor
product.  Its four distinct outside representatives are multiples of those
four factors.  Together with the seven kernel vertices, (15) gives an
eleven-point product cover for the generic four-defect kernel.

## 8. Scope

This closes the simultaneous-placement gap in the `K_(3,4)-e` kernel.  This
component does not itself supply:

1. classification, layer certificates, and placement for genuinely new
   inclusion-minimal eleven-edge kernels of Hall deficit two and three;
2. robustness of every required ten-label certificate under the exceptional
   two-adic matching in the corrected aligned injection; or
3. an endpoint-safe aligned construction of ten cover points away from the
   unique midpoint multiple of `M`.

Those dependencies and their separate audit are supplied in
`erdos708_c11_candidate.md`, `erdos708_c11_new_kernels.md`, and
`erdos708_c11_full_audit.py`; they are not being inherited silently from the
published `c_10` proof.
