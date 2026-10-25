# Erdos problem #708 sibling: proof that `c_10=2`

Date: 2026-08-11 (UTC)

## 1. Result and audited inputs

Let `c_n` be the infimum of the real numbers `c` such that, for every set
`A` of `n` distinct positive integers and every interval `J` contained in
`[0,infinity)` of length `c max(A)`, there are `n` distinct positive integers
in `J` whose product is divisible by `prod(A)`.

This note proves

\[
                              \boxed{c_{10}=2}.                       \tag{1}
\]

The inputs are the already published and independently audited facts used for
`c_9=2`:

1. the two-halves interval injection of van Doorn--Li--Tang;
2. the one-defect product-repair lemma;
3. the two-factor repair of `K_(2,4)` and `K_(3,3)-e`; and
4. the **generic nine-edge theorem**: a simple bipartite graph of nine
   distinct labels at most `M`, drawn in an open interval of length `2M`,
   whose edge label is the positive difference of its endpoints and divides
   them, has a nine-point product cover in the interval.

The last statement is exactly Sections 2--6 of the public Round 6 `c_9`
proof, deployed in site commit `3bd90fd` and backed by the independent
checkers in the parent verification directory. It does not include, or need,
that proof's aligned-endpoint construction. The aligned part of the present
proof is the companion document `c10_aligned_repair.md`; it is incorporated
as Section 8 below.

The public private-prime padding theorem gives `c_n>=2` for every fixed
`n>=4`, hence gives the lower half of (1).  The rest of this note proves the
upper half.  This is still only a sibling constant and does not settle the
parent question `g(n)<=2n`.

## 2. Open intervals, multiples, and exact layers

Put `M=max(A)`.  It is enough to work in the interior

\[
                            I=(x,x+2M)                               \tag{2}
\]

of the given interval.  It has the same metric length and is contained in the
given interval, regardless of the endpoint convention.  All its integer
points are positive, including when `x=0`.

For every positive integer `d`, write

\[
                 Z_I(d)=d\mathbb Z\cap I.
\]

Then

\[
                 |Z_I(d)|\geq \left\lceil\frac{2M}{d}\right\rceil-1. \tag{3}
\]

If `d` divides `k` distinct positive integers at most `M`, their quotients by
`d` are distinct, so `kd<=M`.  Equation (3) then gives at least `2k-1`
interval multiples.

We need a strengthening of the overlap lemma used at nine labels.

**Nine-point progression lemma.**  If `d,e<=M/4`, both `Z_I(d)` and
`Z_I(e)` have at least seven points, and

\[
                         |Z_I(d)\cup Z_I(e)|\leq9,                   \tag{4}
\]

then `d=e`.

Indeed, (3) and (4) force `d,e>=2M/10=M/5`; otherwise the corresponding set
would already have at least ten points.  Hence

\[
                    \frac{\max(d,e)}{\min(d,e)}\leq\frac54.          \tag{5}
\]

If `d!=e`, write the reduced ratio as `v/u`, with `v>u`.  Inequality (5)
forces `u>=4` and `v>=5`, and therefore

\[
                 \operatorname{lcm}(d,e)\geq5\min(d,e)\geq M.
\]

The two sets in (4) have at least five common points, but five common
multiples span at least four lcm steps, at least `4M`, inside an interval of
length `2M`, a contradiction.  (The deliberately loose last bound makes the
endpoint issue harmless.)

Now suppose that `x` is not an integer multiple of `M`.  Split the integer
points of `I` into

\[
 B_-=(x,x+M]\cap\mathbb Z,\qquad B_+=(x+M,x+2M)\cap\mathbb Z.
\]

For `a in A`, let `u_a` be the largest multiple of `a` in `B_-`, and draw

\[
                              e_a=(u_a,u_a+a).                        \tag{6}
\]

Both endpoints lie in `I` and are divisible by `a`.  The ten edges are
distinct because their positive differences are the ten distinct labels.
Call the resulting simple bipartite graph `H`.

For every prime power,

\[
 p^k\mid a_e\quad\Longleftrightarrow\quad
 p^k\text{ divides both endpoints of }e.                            \tag{7}
\]

Thus `v_p(a_e)` is the minimum of the two endpoint valuations, and every
label-level graph is vertex-induced.  This exact reverse implication is used
throughout the generic case.

## 3. Nested Hall reduction

Regard the edges of `H` as left vertices and their endpoints as right
vertices.  If all ten edges have distinct endpoint representatives, those ten
points prove the result.  Otherwise choose an inclusion-minimal deficient
edge set `S`.  With `s=|S|`,

\[
                     |N(S)|=s-1,\qquad s\geq6.                       \tag{8}
\]

The lower bound on `s` follows because a bipartite graph on `s-1` vertices
has at most `floor((s-1)^2/4)<s` edges for `s<=5`.

Put `g=gcd(a_e:e in S)`.  The one-defect lemma says

\[
             \prod_{e\in S}a_e\mid g\prod_{v\in N(S)}v.             \tag{9}
\]

For an edge outside `S`, retain only its endpoints outside `N(S)`.  If these
sets have distinct representatives, select them.  Together with `N(S)` they
use nine points.  Since `g` divides `s` labels, (3) gives at least
`2s-1>=11` `g`-multiples, so an unused tenth point proves the result.

If those outside endpoint sets fail Hall, their union with `S` contains an
edge set with neighbor deficit at least two.  Choose an inclusion-minimal such
set `U`.  Then

\[
                         |N(U)|=|U|-2.                               \tag{10}
\]

For the remaining edges, again retain only endpoints outside `N(U)`.  If they
have distinct representatives, we will use the two-factor kernels below.  If
they fail Hall, the same calculation produces an edge set with deficit at
least three; choose an inclusion-minimal such set `W`, so

\[
                         |N(W)|=|W|-3.                               \tag{11}
\]

The equalities in (10)--(11) follow by deleting one edge from a minimal set.

A simple bipartite graph with `e` edges and `e-2` active vertices cannot exist
for `e<=7`, since `floor((e-2)^2/4)<e`.  Hence a two-defect kernel has
`e=8,9`, or `10`.  Similarly, a three-defect kernel has `e=9` or `10`.
Every active vertex of a minimal kernel has degree at least two, since
deleting a degree-one vertex and its edge preserves the deficit.

The rest of the generic proof supplies the required repair factors and then
places them at distinct unused interval points.

## 4. The uniform layer-repair principle

For a kernel `G`, let

\[
                   \delta(K)=\max(0,|E(K)|-|V(K)|)                  \tag{12}
\]

for a vertex-induced subgraph `K` of `G`.  Suppose fixed edge blocks
`B_1,...,B_q` have the property

\[
        \#\{i:B_i\subseteq E(K)\}\geq\delta(K)                     \tag{13}
\]

for every induced `K`.  At each `p^k` label level, assign its
`delta(K)` missing copies of `p` to distinct contained blocks.  Over all
levels and primes this defines positive integers `d_1,...,d_q` such that

\[
 \prod_{e\in E(G)}a_e\mid
       \left(\prod_{v\in V(G)}v\right)d_1\cdots d_q,                \tag{14}
\]

and

\[
                         d_i\mid a_e\quad(e\in B_i).                \tag{15}
\]

To verify (14), at a `p^k` level the labels demand `|E(K)|` copies and the
selected endpoints supply at least `|V(K)|`; retaining only the positive
level deficits can only overestimate what is missing.  For (15), a copy can
be assigned to block `B_i` only at a level containing every edge of `B_i`,
so the total number assigned is at most the minimum edge valuation on that
block.  This proves the principle for arbitrary, unbounded valuations.

## 5. Two-defect kernels

For eight edges on six vertices, minimality gives exactly the inherited hard
graphs `K_(2,4)` and `K_(3,3)-e`.  They have two disjoint four-edge blocks
satisfying (13).

For nine edges on seven vertices, minimality excludes an eight-edge/six-vertex
kernel.  The published `c_9` classification gives a `3 by 4` graph of balanced
or unbalanced type, with disjoint blocks of sizes four and five satisfying
(13).

It remains to record the new finite lemma.

**Ten-edge/two-defect lemma.**  Every inclusion-minimal ten-edge bipartite
graph on eight active vertices has two disjoint four-edge blocks satisfying
(13).

Here is a complete finite proof.  Minimum degree two rules out bipartition
`2+6`, leaving `3+5` and `4+4`.  In the `3+5` case every vertex on the
five-side has degree two.  Replacing such a vertex by the pair of its row
neighbors reduces the classification to the three partitions
`5=3+2=3+1+1=2+2+1`.  In the `4+4` case the bipartite complement has six edges
and maximum degree two, hence is a disjoint union of paths and even cycles;
discarding the types with a proper two-defect induced subgraph leaves seven
types.  Up to row and column permutations (and transpose in the square case),
the ten matrices are the following.  A row string is an adjacency row; the
two following edge lists are the blocks `P,Q`.

```text
3x5
11111/11100/00011  P=00,01,02,10  Q=03,04,23,24
11110/11101/00011  P=00,01,02,10  Q=03,14,23,24
11110/11001/00111  P=00,01,02,10  Q=03,14,23,24

4x4
1111/1100/1100/0011  P=00,01,02,03  Q=10,11,20,21
1111/1100/1010/1001  P=00,01,10,11  Q=02,03,20,22
1111/1100/1010/0101  P=00,01,02,20  Q=03,10,11,31
1110/1110/1001/0101  P=00,01,02,10  Q=11,20,23,31
1110/1101/1010/0101  P=00,01,02,10  Q=11,13,31,33
1110/1101/1010/0011  P=00,01,02,10  Q=13,20,22,32
1110/1101/0011/0011  P=00,01,02,10  Q=13,22,23,32
```

For each displayed row, direct deletion of row and column subsets verifies
that every positive-excess proper induced subgraph contains `P` or `Q`, and
the full graph, of excess two, contains both.  This is (13).  The companion
audit independently enumerates all 210 labelled `3 by 5` kernels and all
2,040 labelled `4 by 4` kernels, reconstructs the ten isomorphism classes,
and checks every one of the at most 256 induced levels.

Apply Section 4 to any two-defect kernel.  We obtain repair factors `r,s`; in
all cases each is supported on at least four labels, their support blocks are
disjoint, and their union contains at least eight labels.  Thus

\[
                              r,s\leq M/4.                            \tag{16}
\]

If the kernel has `e` edges, the distinct representatives of the remaining
`10-e` edges and its `e-2` vertices form an eight-point set `F`.

Each factor has a multiple outside `F`.  Suppose, for example, that all
`r`-multiples lay in `F`.  There are at least seven of them.  For `e=9` or
`10`, at least six or seven kernel vertices are therefore `r`-divisible;
deleting at most one vertex from the kernel leaves at least five induced
edges.  For `e=8`, at least five kernel vertices are divisible.  In
`K_(2,4)`, the four-edge support already uses both row vertices and two
columns, so a fifth kernel vertex raises the induced edge count to at least
six.  In `K_(3,3)-e`, every advertised support touches five vertices and their
induced graph has at least five edges.  By the exact difference identity,
`r` consequently divides at least five labels.  Then `r<=M/5`, and (3) gives
at least nine interval multiples, contradicting `Z_I(r) subseteq F`.

Finally, if the two outside multiple sets did not have distinct
representatives, their union outside `F` would have size at most one.  Hence

\[
                         |Z_I(r)\cup Z_I(s)|\leq9.
\]

The nine-point progression lemma gives `r=s`.  This common factor divides at
least the eight labels in the union of the two support blocks, so it has at
least fifteen interval multiples, another contradiction.  Two distinct
repair points outside `F` now complete every two-defect case.

## 6. Three-defect kernels other than `K_(2,5)`

A nine-edge/three-defect kernel has six vertices and is `K_(3,3)`.  Its one
remaining edge has an endpoint outside the core, since the core is already
complete.  Select one such endpoint.  The inherited `K_(3,3)` certificate
uses three four-edge `K_(2,2)` blocks `D_i`, obtained by deleting paired row
and column `i`.  Every pair of blocks has seven edges in its union and all
three have nine.

A ten-edge/three-defect kernel has seven vertices. Apart from `K_(2,5)`, it
is `K_(3,4)` with two edges deleted. The inclusion-minimal cases have the
same-row or disjoint deletion types. The same-column type contains a proper
`K_(3,3)` core and is therefore redundant, but its displayed certificate is
valid and is retained as an extra check. The following table gives three
four-edge blocks; omitted edges are listed first.

```text
same row, omit 00,01:
  B1=02,03,12,13  B2=10,11,20,21  B3=12,13,22,23

disjoint, omit 00,11:
  B1=01,02,12,21  B2=02,03,22,23  B3=10,13,20,23

same column, omit 00,10:
  B1=01,02,11,12  B2=01,03,21,23  B3=12,13,22,23
```

Checking the row/column subsets gives (13): every induced excess is supported
by at least that many displayed blocks.  Every pairwise block union has at
least six edges, and the union of all three has at least nine.  These three
types account for all 66 choices of the two omitted edges. Exactly 54 are
inclusion-minimal three-defect kernels; the other 12 are the redundant
same-column cases. Row/column symmetry reduces the certificate check to the
three displayed representatives.

Section 4 supplies three repair factors, each supported on four labels and
hence at most `M/4`.  The six core vertices plus the outside endpoint in the
`K_(3,3)` case, or the seven kernel vertices in the ten-edge case, form a
seven-point set `F`.

Each factor has an outside multiple.  Otherwise its at least seven multiples
would be exactly `F`, making all kernel vertices divisible by it.  By (7) it
would divide all nine core labels or all ten kernel labels, which gives far
more than seven interval multiples.

Hall for the three outside-multiple sets is now immediate from the progression
lemma.  If a pair had outside union of size at most one, its full union would
have size at most eight, so the two factors would be equal.  Their common
value divides at least six labels and therefore has at least eleven interval
multiples, a contradiction.  If all three had outside union of size at most
two, their full union would have size at most nine.  Applying the progression
lemma pairwise makes all three factors equal.  Their common value divides at
least nine labels, again a contradiction.  Hall supplies three distinct
repair points outside `F`.

## 7. The exceptional `K_(2,5)` kernel

Fixed four-edge blocks do **not** repair every induced layer of `K_(2,5)`;
asserting otherwise is the main tempting gap at ten labels.  We use a
different certificate.

Write the vertices as `L_1,L_2,R_1,...,R_5`, and let `a_ij` be the label on
`L_iR_j`.  Put

\[
                         q_j=\gcd(a_{1j},a_{2j})                    \tag{17}
\]

and

\[
              R=\gcd\left(q_iq_jq_k:1\leq i<j<k\leq5\right).       \tag{18}
\]

Then

\[
 \prod_{i=1}^2\prod_{j=1}^5 a_{ij}\mid
        L_1L_2R_1\cdots R_5\,R.                                    \tag{19}
\]

For a prime `p`, let the endpoint valuations be `l_1,l_2,r_j`.  Exactness
(7) gives

\[
 v_p(a_{ij})=\min(l_i,r_j),\qquad
 v_p(q_j)=\min(l_1,l_2,r_j).                                       \tag{20}
\]

At a level where both left vertices and `t` columns survive, the positive
edge/vertex excess is `max(0,t-2)`; no other level has positive excess.  If
the five values `v_p(q_j)` are put in increasing order, summing these excesses
over all levels gives the sum of the three smallest.  This is exactly
`v_p(R)`, since (18) minimizes over all triple products.  This proves (19) for
arbitrary valuations.

It remains to choose three distinct unused interval points whose product is
divisible by `R`.  It is enough to choose any three distinct indices and
distinct unused multiples of their `q_j`, because `R` divides every triple
product in (18).

Consider the bipartite graph from the five indices to their `q_j`-multiples
outside the seven kernel vertices.  It has a matching of size at least three.
Suppose not.  By Konig's theorem it has a vertex cover consisting of `h`
indices and `t` outside points, with `h+t<=2`.  For each of the remaining
`5-h` indices, all unused `q_j`-multiples lie among the same `t` points.

Let `D=|L_1-L_2|`.  Equation (17) and the edge differences give `q_j|D`.
Between `L_1` and `L_2` there are `D/q_j-1` further `q_j`-multiples.  They
are in the left half, are not kernel vertices, and hence belong to those `t`
points.  Therefore

\[
                         D/q_j\in\{1,\ldots,t+1\}.                  \tag{21}
\]

Group the remaining columns according to `q_j=D/m`, and let `n_m` be the
group sizes.  If group `m_0` is nonempty, `D/m_0` divides both labels in every
group whose index divides `m_0`.  Its full interval-multiple set has at most
`7+t` points.  If

\[
                         C=\sum_{m\mid m_0}n_m,
\]

then it divides `2C` distinct labels, so (3) gives at least `4C-1` multiples.
Consequently `4C-1<=7+t`.

There are only three cases.  If `t=0`, at least three remaining columns all
have `m=1`, giving `C>=3`, impossible.  If `t=1`, at least four remaining
columns have `m=1` or `2`; the largest nonempty group index captures all of
them and again gives `C>=4`.  If `t=2`, all five columns remain and have
indices `1,2,3`.  A nonempty group `2` gives `n_1+n_2<=2`, and a nonempty
group `3` gives `n_1+n_3<=2`; if both occur their sum contradicts
`n_1+n_2+n_3=5`. If exactly one is absent, the other inequality already sees
all five columns. If both are absent, then `n_1=5`; taking `m_0=1` gives
`C=5`, again impossible. This contradiction proves the matching claim.

Select the resulting three unused multiples.  With the seven kernel vertices,
(19) gives a ten-point cover of `K_(2,5)`.

Sections 3--7 complete the generic case.

## 8. The aligned endpoint case

The full aligned proof is `c10_aligned_repair.md`, incorporated here by
reference. It is separate because a first draft made an invalid inference:
if a nine-point product is divisible by `prod(A minus {M})` and contains the
midpoint `b_0=x+M`, the same occurrence of `b_0` cannot also be counted afresh
to supply `M`. The hostile audit gives an explicit `M=10` counterexample to
that inference.

The repaired proof instead uses the corrected van Doorn--Li--Tang injection
for the nine labels below `M`. All nine edges and all nine selected cover
points avoid `b_0`. The only failure of exact prime-power support is one
surplus two-adic level on certain symmetric type-(22c) edges; those exceptional
edges form a matching. The companion proof shows that the `4+5`, `K_(3,3)`,
and inherited hard-core repair certificates remain valid after deleting any
such exceptional matching from an endpoint-induced level.

Because every smaller label is at most `M-1`, a factor dividing `k` of them
has at least `2k` interval multiples. The companion proof redoes the one-,
two-, and three-factor placement arguments with `b_0` added to the forbidden
set. It obtains nine distinct points in `I minus {b_0}` whose product covers
`prod(A minus {M})`; adjoining `b_0` then supplies a genuinely new factor
divisible by `M`. This proves the aligned case without valuation reuse.

Together with the generic case and the existing lower bound, this proves
(1), with open endpoints and positivity accounted for.

## 9. Finite audit

`verify_c10_graph_layers.py` checks:

- all 210 labelled `3 by 5` and 2,040 labelled `4 by 4` ten-edge/two-defect
  kernels, including the ten isomorphism types and their block certificates;
- all 54 minimal and 12 redundant `K_(3,4)`-minus-two-edge deletion patterns
  through their three symmetry types and displayed certificates;
- 655,360 capped endpoint-valuation vectors across the ten two-defect types;
- 49,152 capped vectors across the three `K_(3,4)` types, plus 4,096 inherited
  `K_(3,3)` vectors;
- all `6^7=279,936` capped endpoint patterns for the `K_(2,5)`
  order-statistic formula; and
- 1,164,320 distinct small progression pairs, including half-integral phases,
  for the nine-point progression lemma.

`verify_c10_aligned_repair.py` checks the exceptional two-adic layer
description, 3,888 no-core graph/matching pairs, all 34 `K_(3,3)` exceptional
matchings, hard-core placement cases, corrected-injection arithmetic, and
strict forbidden-midpoint counts. `verify_c10_cold_audit.py` independently
rebuilds the graph classifications and aligned checks, including 48,048
literal small forbidden-midpoint instances.

These computations certify the finite tables and stress the valuation and
placement formulas. The written proofs, rather than bounded valuation loops,
cover arbitrary interval scales and prime-adic valuations.

## Source

W. van Doorn, Y. Li, and Q. Tang, *Optimal bounds for an Erdos problem on
matching integers to distinct multiples*, arXiv:2603.28636 (2026), especially
Section 4: https://arxiv.org/abs/2603.28636

The generic `c_9` product-cover theorem used above is proved in the public
Round 6 article and its verification bundle; it is not claimed as a theorem
of van Doorn--Li--Tang.
