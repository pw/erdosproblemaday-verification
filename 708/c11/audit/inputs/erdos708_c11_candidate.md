# Erdos problem #708 sibling: candidate proof that `c_11=2`

Date: 2026-08-11 UTC

Status: complete candidate, pending an independent cold audit.  The genuinely
new finite classifications and the four-defect placement proof are in the
companion files named in Section 10.

## 1. Result and audited inputs

Let `c_n` be the infimum of the real numbers `c` such that, for every set
`A` of `n` distinct positive integers and every interval contained in
`[0,infinity)` of length `c max(A)`, there are `n` distinct positive integers
in the interval whose product is divisible by `prod(A)`.  This note proves,
subject to the finite audits listed below,

\[
                              \boxed{c_{11}=2}.                     \tag{1}
\]

We use the following published inputs from the audited `c_10` proof.

1. The generic and corrected aligned interval injections of van Doorn--Li--Tang.
2. The one-defect product-repair lemma, which needs only that every edge label
   divide both endpoints.
3. The complete two-defect certificates through ten edges and the complete
   three-defect certificates through ten edges, with the exceptional
   `K_(2,5)` order-statistic certificate.
4. The private-prime padding theorem, which gives `c_n>=2` for every fixed
   `n>=4`.

The new inputs proved and exhaustively checked here are:

1. the eleven-edge two- and three-defect classifications and certificates;
2. the simultaneous four-factor placement lemma for `K_(3,4)-e`;
3. the joint endpoint/repair product-placement lemma below; and
4. robustness of every needed ten-edge aligned certificate under the
   exceptional two-adic matching.

## 2. Interval counts and the two injections

Put `M=max(A)` and work in the interior

\[
                              I=(x,x+2M).                            \tag{2}
\]

For a positive integer `d`, write \(Z(d)=d\mathbb Z\cap I\).  Then

\[
                    |Z(d)|\ge\left\lceil{2M\over d}\right\rceil-1. \tag{3}
\]

If `d` divides `k` distinct labels at most `M`, then `kd<=M` and

\[
                              |Z(d)|\ge2k-1.                        \tag{4}
\]

If all those labels are at most `M-1`, then `kd<=M-1`, so

\[
                              |Z(d)|\ge2k.                          \tag{5}
\]

First suppose `x` is not an integer multiple of `M`.  For every \(a\in A\),
let `u_a` be the largest multiple of `a` in `(x,x+M]` and draw the edge

\[
                              (u_a,u_a+a).                           \tag{6}
\]

These eleven edges are distinct, cross the two halves of `I`, and have the
exact prime-power property

\[
 v_p(a_e)=\min(v_p(y_e^-),v_p(y_e^+)).                              \tag{7}
\]

The generic proof occupies Sections 3--7.

If `x` is a multiple of `M`, put `b_0=x+M`, reserve this unique interior
multiple of `M`, and put \(A_0=A\setminus\{M\}\).  Section 8 uses the corrected
aligned injection on the ten labels of `A_0`; all of its endpoints avoid
`b_0`.

## 3. Maximum-defect reduction

For a set `S` of edges in the injection graph, put

\[
                              d(S)=|S|-|N(S)|.
\]

Let `q=max_S d(S)`, with the empty set showing `q>=0`.  If `q=0`, Hall's
theorem gives distinct endpoint representatives for every edge.

Suppose `q>0`, and choose an inclusion-minimal edge set `K` with `d(K)=q`.
Write

\[
 e=|K|,\qquad V=N(K),\qquad |V|=e-q,\qquad T=E(H)\setminus K.       \tag{8}
\]

Every active vertex of `K` has degree at least two.  For every \(R\subseteq T\),
maximality of `q` gives

\[
 |N(R)\setminus V|\ge|R|,                                         \tag{9}
\]

because otherwise \(d(K\cup R)>q\).  Thus the endpoint sets

\[
                         Y_e=N(e)\setminus V\quad(e\in T)           \tag{10}
\]

have a system of distinct representatives.

The bipartite edge bound and minimum degree give the following exhaustive
list.  Here only active vertices are counted.  A defect-zero component could
be removed without changing the defect, a negative-defect component could be
removed to increase it, and two positive-defect components would each need
at least six edges.  Thus a minimal core with at most eleven edges has just
the active component classified below.  Since a simple bipartite graph on
\(e-q\) active vertices has at most \(\lfloor(e-q)^2/4\rfloor\) edges, the
listed ranges follow; for \(q=4,e=11\), equality of the part-size bound
forces parts of sizes 3 and 4 and exactly one missing edge.

```text
q=1: e>=6;
q=2: e=8,9,10,11;
q=3: e=9,10,11;
q=4: e=11, and K=K_(3,4)-e;
q>=5: impossible.
```

For `q=2`, every fixed-block certificate supplies factors `d_1,d_2`; each
support has at least four edges and the two support unions have at least six.
For `q=3`, outside the exceptional `K_(2,5)`, the certificates supply three
factors supported on four-edge blocks; pairwise support unions have at least
six edges and the three-block union has at least nine.  At every such fixed
block `B` we also use

\[
                  |B\cup E(K-v)|\ge5\qquad(v\in V).                \tag{11}
\]

For `e<=10`, we use the classifications and block sizes published in the
`c_8`--`c_10` proofs.  The full companion audit searches those finite block
families and verifies the level conditions, support unions, and (11) for
every class.  For `e=11`, the new companion classification contains eleven
two-defect `4 x 5` classes, three three-defect `3 x 5` classes, and eight
three-defect `4 x 4` classes.  Its checker verifies (11) and every
endpoint-induced level for every class.

## 4. Progression lemmas

We use the published nine-point progression lemma and the following slight
extension.

**Ten-point progression lemma.**  If `d,e<=M/4`, each of `Z(d),Z(e)` has at
least seven points, and

\[
                              |Z(d)\cup Z(e)|\le10,                 \tag{12}
\]

then `d=e`.

Indeed, (12) forces `d,e>=2M/11`.  If their distinct reduced ratio is
`v/u>1`, then

\[
                         {v\over u}\le{M/4\over2M/11}={11\over8},
\]

so `u>=3,v>=4`.  Their lcm is at least `4(2M/11)=8M/11`.  The two sets have
at least four common points, which span at least three lcm steps, more than
the length `2M`.  This is impossible.

## 5. Joint endpoint/repair placement

This section is the mechanism that prevents an extra outside edge at eleven
labels from consuming the only useful repair multiple.

Let `K` be a fixed-block core of defect `q=2` or `3`, with repair factors
`d_1,...,d_q`.  Regard the remaining edges as items with neighborhoods
`Y_e`, and a repair factor as an item with neighborhood
\(Z(d_i)\setminus V\).

Each repair neighborhood is nonempty.  A factor supported on four labels has
at least seven multiples.  This is immediate when `|V|<=6`; when `|V|=7`,
containment makes every core vertex divisible; when `|V|=8`, at least seven
vertices are divisible and (11) makes the factor divide at least five core
labels.  In either latter case (4) gives more multiples than vertices.  A
five-edge support has at least nine multiples; containment among nine
vertices again makes it divide every core label.

Every item subset containing at least two repair factors satisfies Hall.  If
it contains `r` remaining edges and `s>=2` repairs but has outside union at
most `r+s-1`, the full union of those repair progressions has size at most

\[
 |V|+r+s-1\le(e-q)+(11-e)+s-1=10-q+s.                              \tag{13}
\]

For `q=2,s=2`, this is ten.  The ten-point lemma makes the two factors equal;
their support union has at least six labels, giving at least eleven multiples,
contrary to (13).  For `q=3,s=2`, (13) is nine and the published nine-point
lemma gives the same contradiction.  For `q=3,s=3`, (13) is ten; applying
the ten-point lemma pairwise makes all factors equal, while their nine-label
support union gives at least seventeen multiples.

If the whole item family satisfies Hall, its representatives complete the
cover.  Suppose it does not.  Since edge-only subsets satisfy Hall by (9),
and subsets with at least two repairs have just been excluded, a deficient
set has the form

\[
                              J=R\cup\{d\},                         \tag{14}
\]

where `R` consists of `r` remaining edges.  Necessarily

\[
 |N(J)|=|N(R)|=r,\qquad Z(d)\setminus V\subseteq N(R).             \tag{15}
\]

There cannot be deficient sets for two different repair factors.  Indeed,
the deficiency `|S|-|N(S)|` is supermodular; the intersection of two such
sets is edge-only and has nonpositive deficiency, so their union would be a
forbidden subset with two repairs.

Delete the unique bad repair `d`.  The remaining item family satisfies Hall.
Moreover, the tight edge set `R` can be matched onto all `r` points of
`N(R)`, and the other items can be matched outside `N(R)`: for any set `S`
of other items,

\[
 |N(S)\setminus N(R)|
   =|N(S\cup R)|-|N(R)|\ge |S|.                                   \tag{16}
\]

Choose \(z\in Z(d)\setminus V\).  It is one of the `r` points and is matched to
some edge `e_0`.  Put

\[
                              g=\gcd(d,a_{e_0}).                    \tag{17}
\]

The core vertices and the one selected point for every item other than `d`
form exactly ten forbidden points.  There is a `g`-multiple outside them.
Indeed, `g` divides the four support labels of `d` and the distinct label
`a_(e0)`, so it has at least nine multiples.  If all lay among those ten
points, at least `|V|-1` core vertices would be `g`-divisible.  By (11), the
union of the support block and the edges induced after deleting the possible
exceptional vertex has at least five core labels; together with `a_(e0)`,
`g` divides at least six labels.  Equation (4) then gives at least eleven
multiples, a contradiction.  Call an outside multiple `w`.

Use the matched points for every other item, use `z` once, and use `w` as the
extra point.  Since `z` is divisible by both `d` and `a_(e0)`,

\[
             z w\quad\hbox{is divisible by}\quad
             \operatorname{lcm}(d,a_{e_0})\gcd(d,a_{e_0})
             =d a_{e_0}.                                          \tag{18}

Thus the collision loses no valuation and the selected points cover all
remaining edge labels and all repair factors.  This proves the joint
placement lemma.

## 6. Generic defects zero through three

For `q=0`, endpoint representatives give the result.

For `q=1`, let `g` be the gcd of the labels in `K`.  The one-defect lemma
gives

\[
              \prod_{e\in K}a_e\mid g\prod_{v\in V}v.             \tag{19}
\]

Match every remaining edge into \(N(e)\setminus V\) by (9).  These points and
`V` number ten.  Since `g` divides `e>=6` labels, it has at least eleven
multiples; choose one outside the ten points.

For `q=2`, use the two fixed-block factors and Section 5.  For `q=3`, do the
same except when `K=K_(2,5)`.

For that exception, write its rows as `L_1,L_2`, its five columns as `R_j`,
and

\[
 q_j=\gcd(a_{1j},a_{2j}),\qquad
 R=\gcd(q_iq_jq_k:i<j<k).                                         \tag{20}
\]

The published order-statistic calculation gives

\[
 \prod_{i=1}^2\prod_{j=1}^5a_{ij}\mid
 L_1L_2R_1\cdots R_5 R.                                           \tag{21}

There is one remaining edge.  Choose any endpoint `y` outside the seven core
vertices; (9) guarantees one.  The five `q_j`-multiple sets outside the
eight-point set \(V\cup\{y\}\) have matching number at least three.  Here is
the strengthened order argument.

If not, Konig gives a cover of `h` indices and `t` outside points with
`h+t<=2`.  For every uncovered index, put `D=|L_1-L_2|` and `m=D/q_j`.
The internal progression can meet the extra forbidden point `y` at most
once, so

\[
                         m\le t+2,\qquad
 P_m\subseteq\{y\}\cup T.                                        \tag{22}
\]

If `n_m` counts the uncovered indices and `m_0` occurs, then `D/m_0`
divides the two labels in every group with `m|m_0`.  Since all its multiples
lie among `8+t` points,

\[
                         4\sum_{m\mid m_0}n_m-1\le8+t,             \tag{23}
\]

so every divisor capture has size at most two.  If `t=0`, at least three
indices remain with \(m\in\{1,2\}\); an occurring largest denominator
captures all of them, contradicting (23).  If `t=1`, at least four remain
with \(m\in\{1,2,3\}\).  If both 2 and 3 occur, then
\(|P_2\cup P_3|=3>2\); otherwise an occurring nonunit denominator, or 1 if
there is none, captures all four.  If `t=2`, all five remain and
\(m\le4\).  An occurrence of 4 excludes 3 because
\(|P_4\cup P_3|=5>3\), after which 4 captures every occurrence of 1, 2,
or 4, so there are at most two.  Without 4, occurrences of both 2 and 3
would satisfy \(n_1+n_2\le2\) and \(n_1+n_3\le2\), and hence total at most
four; if either is absent, the other occurring denominator captures all
five.  (The unique four-occurrence extremal multiplicities are
\(n_2=n_3=2\).)  This contradiction proves the matching claim.

Select three such multiples away from `y`; their product is divisible by
`R`.  Together with the seven core vertices and `y`, (21) gives eleven
points.

## 7. The generic four-defect kernel

Here `K` is all eleven edges of `K_(3,4)-e`, so there are no remaining edge
items.  The finite layer certificate defines `R` as the gcd of 45 products

\[
 q_{01,a}q_{02,b}q_{12,c}q_{12,d},\quad c\ne d,\quad
 \neg(a=b\text{ and }a\in\{c,d\}),                                \tag{24}
\]

and proves

\[
 \prod_{e\in K}a_e\mid\left(\prod_{v\in V}v\right)R.             \tag{25}
\]

The companion placement proof forms the transversal matroid of all ten pair
blocks and proves the ranks

\[
 r(A),r(B)\ge1,\quad r(C)\ge3,\quad r(A\cup B)\ge2,
\]
\[
 r(A\cup C),r(B\cup C)\ge4,\quad r(A\cup B\cup C)\ge5.            \tag{26}
\]

Rado's theorem selects one `A`, one `B`, and three `C` blocks with five
distinct outside multiples.  If the `A,B` columns differ, discard any `C`
block.  If they agree in column `j` and `C_j` was selected, discard `C_j`;
if they agree but `C_j` was not selected, discard any selected `C` block.
The four retained blocks satisfy (24) and retain distinct representatives.
Their product is a multiple of `R`, so (25) completes the generic case.

## 8. The aligned endpoint

Assume now `x` is a multiple of `M`, reserve `b_0=x+M`, and apply the
corrected aligned injection to the ten labels `a<M`:

\[
 (u_a,u_a+a)\quad(a\nmid b_0),
\]
\[
 (b_0-2a,b_0+2a)\quad(a\mid b_0,\ 2a<M,\ 2a\nmid b_0),
\]
\[
 (b_0-a,b_0+a)\quad\hbox{otherwise}.                              \tag{27}
\]

The ten edges are simple, cross the halves, and avoid `b_0`.  Exactness can
fail only at one surplus two-adic level on an edge of the last type with
`b_0/a` odd.  Those exceptional edges form a matching `X`.  At every
prime-power level the actual label graph is therefore

\[
                              L=K[W]\setminus Y,\qquad Y\subseteq X,\tag{28}
\]

with endpoint supply `|W|`.

We need the following new finite robustness lemma.

**Aligned robustness lemma.**  For every inclusion-minimal two-defect core
with 8, 9, or 10 edges, and every matching `X` in it, there are two support
blocks of the published sizes such that for every `W` and every
\(Y\subseteq X\cap E(K[W])\),

\[
 \#\{B:B\subseteq E(K[W])\setminus Y\}
       \ge\max(0,|E(K[W])\setminus Y|-|W|).                         \tag{29}
\]

The analogous statement holds for the fixed-block three-defect cores with
9 or 10 edges.  The blocks retain pairwise union at least six, total
three-block union at least nine, and the endpoint-safe property

\[
              |B\cup(E(K-v)\setminus X)|\ge5\qquad(v\in V).       \tag{30}
\]

The independent checker enumerates every core isomorphism class, every
matching `X`, every endpoint subset `W`, and every active subset `Y`, and
discovers a valid certificate.  This is a finite lemma, not an assumption of
generic exactness.

Assign prime-power deficits only to blocks contained in the actual graph
`L`.  Formula (29) supplies enough blocks, and every accumulated factor
divides every actual label in its support.  Thus the same product repair is
valid in the aligned graph.

The maximum-defect reduction (8)--(10) is purely graph-theoretic and still
applies.  All endpoint neighborhoods avoid `b_0`.  For `q=0`, use endpoint
representatives.  For `q=1`, the one-defect lemma needs only endpoint
divisibility; after matching the remaining edges, the core vertices,
matched points, and `b_0` are ten forbidden points.  The gcd divides at
least six labels below `M`, so (5) gives at least twelve multiples.

For a fixed-block `q=2` or `3` core, repeat Section 5 with every repair
neighborhood also excluding `b_0`.  Equation (13) is unchanged, because the
aligned graph has ten edges but the base forbidden set has the extra point:

\[
 (e-q)+1+(10-e)+s-1=10-q+s.                                      \tag{31}
\]

Singleton repair neighborhoods are nonempty.  A four-label factor now has
at least eight multiples by (5).  The only near-equality case is a ten-edge
two-defect core: at least seven of its eight vertices are divisible.  By
(30), a nonexceptional edge outside the support is induced, making the
factor divide a fifth label and giving at least ten multiples.  The smaller
cores are easier; equality forces all core vertices divisible, and (30)
again supplies a fifth nonexceptional label.

The collision construction also remains valid.  Its gcd `g` divides five
labels below `M`, so it has at least ten multiples.  If all were the ten
already selected or forbidden points, every core vertex would be divisible
by `g`; (30) supplies a nonexceptional fifth core label outside the
four-edge support, in addition to the collided outside label.  Thus `g`
divides six labels and has at least twelve multiples.  A new `w` exists, and
(18) proves the product divisibility without reusing a point.

It remains to check the aligned `K_(2,5)`.  Formula (21) is robust under
(28).  At a level with both rows and `c` endpoint columns, let `y` exceptional
matching edges be deleted.  They lie in distinct columns, so the number of
columns retaining both actual labels is `t=c-y`, and

\[
 \max(0,|E(L)|-|W|)=\max(0,2c-y-(2+c))=\max(0,t-2),                \tag{32}
\]

exactly the contribution supplied by the three-smallest order statistic in
(20).  With `b_0` adjoined to the seven core vertices, the strengthened
argument (22)--(23) applies verbatim.  In fact (5) gives the stronger bound
`4C` in place of `4C-1`.  It supplies three distinct repair multiples away
from `b_0`.

We have therefore constructed ten distinct points in \(I\setminus\{b_0\}\) whose
product `P_0` is divisible by `prod(A_0)`.  Since `M|b_0`, adjoining `b_0`
gives eleven distinct points and

\[
                              \prod(A)\mid P_0b_0.                  \tag{33}
\]

This completes the aligned case without counting any valuation from `b_0`
twice.

## 9. Conclusion

The generic and aligned cases prove `c_11<=2`.  The private-prime padding
theorem gives `c_11>=2`, proving (1).

## 10. Verification artifacts

The new artifacts are:

```text
erdos708_c11_placement_candidate.md
erdos708_c11_placement_audit.py
erdos708_c11_new_kernels.md
erdos708_c11_new_kernels_audit.py
erdos708_c11_full_audit.py
```

The first audit checks the 45 admissible four-defect products, all capped
endpoint valuation vectors, every finite confined-grid case used in (26),
and literal exact-difference kernels.  The second independently enumerates
13,560 labelled new two-defect kernels and 2,694 labelled new three-defect
kernels, reconstructs all 22 table classes, and verifies both their
endpoint-level certificates and the collision-safe condition (11).  The full
audit checks the
inherited-core collision condition, the aligned robustness lemma, the
strengthened `K_(2,5)` grid cases, and the joint-placement arithmetic.

No bounded arithmetic search is used in place of the open-interval,
Konig/Hall, Rado, or prime-power layer arguments written above.
