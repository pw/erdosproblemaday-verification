# Replacement for Section 8: the aligned endpoint

This note replaces Section 8 of `erdos708_c10_candidate.md`.  The original
argument at lines 462--466 is invalid: if a nine-point product `P` is divisible
by `prod(A minus {M})` and contains a point divisible by `M`, it does not follow
that `P` is divisible by `M prod(A minus {M})`.  Prime powers supplied by that
point may already have been used to cover the smaller labels.

The repair below constructs the nine-point cover away from the midpoint and
only then adds the midpoint.  It uses the corrected aligned injection of van
Doorn--Li--Tang and a small robustness observation for its exceptional
two-adic layers.

## 8. The aligned endpoint case

Suppose that `x` is an integer multiple of `M`, and put

\[
                              b_0=x+M.
\]

Then `b_0` is a positive point of `I=(x,x+2M)` divisible by `M`.  Put
`A_0=A minus {M}`.  Thus `A_0` consists of nine distinct positive integers,
all at most `M-1`.

For `a in A_0`, let `u_a` be the largest multiple of `a` in `(x,x+M]`.
Use the corrected aligned pair

\[
 (u_a,u_a+a)\qquad(a\nmid b_0),                                      \tag{22a}
\]

\[
 (b_0-2a,b_0+2a)\qquad
 (a\mid b_0,\ 2a<M,\ 2a\nmid b_0),                                  \tag{22b}
\]

and

\[
 (b_0-a,b_0+a)\qquad\text{otherwise}.                               \tag{22c}
\]

The aligned construction of van Doorn--Li--Tang proves that these nine pairs
are distinct, cross the two halves, lie in `I minus {b_0}`, and have both
endpoints divisible by their label.  Call the resulting simple bipartite graph
`H`.

### 8.1 The only failure of exactness

For an edge `e` of type (22b) or (22c), write `q=b_0/a_e`.  At every odd prime
the endpoint difference, which is `4a_e` or `2a_e`, gives

\[
 v_p(a_e)=\min(v_p(y_e^-),v_p(y_e^+)).                               \tag{23}
\]

The same equality holds at `p=2` except in the following case:

\[
 e\text{ has type (22c) and }q\text{ is odd}.                        \tag{24}
\]

Indeed, in type (22b), `q` is odd and the endpoint quotients are `q-2,q+2`,
which are odd.  In type (22c), the quotients are `q-1,q+1`.  If `q` is even,
both are odd.  If `q` is odd, both are even and exactly one is divisible by
only one power of two.  Consequently

\[
 \min(v_2(y_e^-),v_2(y_e^+))=
 \begin{cases}
 v_2(a_e)+1,&e\text{ satisfies (24)},\\
 v_2(a_e),&\text{otherwise}.
 \end{cases}                                                         \tag{25}
\]

If (24) holds, then `2a_e\nmid b_0`, so the definition of type (22c) forces
`2a_e>=M`; equality would make `q=2(x/M+1)` even.  Hence every exceptional
label is strictly larger than `M/2`.  More importantly, its edge is

\[
                         (b_0-a_e,b_0+a_e).
\]

Distinct exceptional labels therefore have distinct left and right endpoints.
The exceptional edge set `X` is a matching.

Fix a prime-power level.  For odd primes the label-level graph is exactly the
subgraph induced by the divisible endpoints.  At a `2^k` level it is

\[
                         L=K\setminus Y,                              \tag{26}
\]

where `K` is the endpoint-induced graph and

\[
       Y=\{e\in X:v_2(a_e)=k-1\}\cap E(K)
\]

is a matching.  Each exceptional edge is deleted at exactly its one surplus
endpoint level and nowhere else.

### 8.2 Robustness of the nine-edge repair certificates

The one-defect lemma and the inherited eight-edge hard-graph lemma require
only that every edge label divide its endpoints.  They therefore apply to
`H` without change.  Only the two new certificates from the generic `c_9`
proof need checking against (26).

At a level let `W` be the full set of divisible graph vertices.  The endpoint
product supplies `|W|` copies of the prime, whether or not some of those
vertices become isolated after the deletion in (26).  Thus the number of
copies still needing repair is at most

\[
                         \Delta(L,W)=\max(0,|E(L)|-|W|).              \tag{27}
\]

First let `G` be one of the nine-edge/seven-vertex graphs with no inherited
eight-edge hard core.  Its published certificate partitions its edges into
blocks `P,Q` of sizes four and five.  Every proper endpoint-induced subgraph
has active edge/vertex excess at most one and, when that excess is positive,
contains `P` or `Q`.

If `K` is proper and `Y` is empty, use that certificate.  If `K` is proper and
`Y` is nonempty, deleting one demanded edge while retaining all endpoint
contributions makes (27) zero.  If `K=G`, then `W=V(G)` and

\[
                         \Delta(L,W)=\max(0,2-|Y|).                   \tag{28}
\]

For `Y` empty both blocks are present.  For `|Y|=1`, the omitted edge belongs
to exactly one member of the partition `P,Q`, so the other block is present.
For `|Y|>=2`, (28) is zero.  Hence the same fixed blocks support every aligned
prime-power layer.

Now let `G=K_(3,3)`.  Choose a perfect pairing between its rows and columns
that is disjoint from the exceptional matching `X`.  Such a pairing exists:
extend `X` to a perfect matching and take either cyclically shifted perfect
matching.  For each paired row and column let `D_i` be the four-edge
`K_(2,2)` left after deleting them.

The proper induced levels are handled as before; one deleted exceptional edge
eliminates their possible excess one.  At the full level the required number
is `3-|Y|`.  Because the chosen pairing avoids `X`, every exceptional edge is
off the pairing and belongs to exactly one of the three blocks `D_i`.
Deleting `|Y|` exceptional edges therefore destroys at most `|Y|` blocks and
leaves at least `3-|Y|` available blocks.  The three-factor certificate is
also robust.

At each level assign `Delta(L,W)` copies to distinct available blocks.  Summed
over all levels, these copies cover the entire difference between label demand
and endpoint supply, because the endpoint product supplies `sum_k |W_k|`.
A copy is assigned to a block only when every label in that block belongs to
the actual label-level graph `L`, not merely to the endpoint supergraph `K`.
Consequently the exponent accumulated in a factor is at most the valuation of
every label in its fixed block.  The resulting factors therefore give exactly
the product inequalities and support divisibilities of the generic nine-edge
proof, for arbitrary valuations.

### 8.3 Choosing every repair point away from `b_0`

We use the strict version of the interval-multiple count.  If `d` divides `k`
distinct labels of `A_0`, then

\[
                         kd\leq M-1,
\]

and hence

\[
 |Z_I(d)|\geq\left\lceil\frac{2M}{d}\right\rceil-1\geq2k.           \tag{29}
\]

Apply the structural reduction from the generic nine-edge proof to `H`.

If `H` has a matching saturating all nine edges, its nine endpoint
representatives already avoid `b_0`.

In a one-defect case the selected graph vertices use eight points.  The repair
gcd divides `s>=6` labels, so (29) gives at least `2s>=12` multiples.  One can
be chosen outside the eight selected points and `b_0`.

Next suppose there is an inherited eight-edge hard core and choose an outside
endpoint of the ninth edge.  These form a seven-point set `F`, disjoint from
`b_0`.  The hard-core factors `r,s` are supported on complementary four-edge
blocks, so each has at least eight interval multiples by (29).

Each factor has a multiple outside `C=F union {b_0}`.  Otherwise its at least
eight multiples would equal the eight points of `C`, making all six core
vertices divisible by it.  The complementary four-edge core block contains a
nonexceptional edge, because the exceptional edges form a matching and a
six-vertex graph has matching number at most three.  Exactness on that edge
makes the factor divide a fifth distinct label.  Equation (29) would then give
at least ten multiples, contradicting containment in `C`.

The two outside multiple sets have distinct representatives.  Otherwise their
outside union has size at most one, so

\[
                         |Z_I(r)\cup Z_I(s)|\leq9.
\]

The nine-point progression lemma makes `r=s`.  The common value divides all
eight labels in the two complementary support blocks, so (29) gives at least
sixteen multiples, a contradiction.

For a nine-edge/seven-vertex graph with blocks `P,Q`, let `r` be supported on
the four-edge block and `s` on the five-edge block.  Put
`C=V(H) union {b_0}`, so `|C|=8`.  Equation (29) gives at least ten
`s`-multiples, hence at least two outside `C`.  The factor `r` also has an
outside multiple.  If not, its at least eight multiples would equal `C`, so
all seven graph vertices would be `r`-divisible.  The five-edge block contains
a nonexceptional edge because an exceptional matching on seven vertices has
at most three edges.  Exactness on that edge makes `r` divide a fifth label,
giving at least ten multiples, a contradiction.  Choose an outside
`r`-multiple and then a different outside `s`-multiple.

Finally suppose `H=K_(3,3)`.  Put `C=V(H) union {b_0}`, so `|C|=7`.  Each of
the three four-block factors has at least eight multiples and therefore has an
outside point.  If a pair of outside neighborhoods had union at most one, the
full multiple-set union would have size at most eight.  The nine-point
progression lemma would make the factors equal; their common value divides the
seven labels in the union of their blocks, so (29) gives at least fourteen
multiples, a contradiction.  If all three outside neighborhoods had union at
most two, their full union would have size at most nine.  Applying the same
lemma pairwise makes all three factors equal.  Their common value divides all
nine labels, so (29) gives at least eighteen multiples, again a contradiction.
Hall's theorem supplies three distinct repair points outside `C`.

Thus every structural case gives nine distinct points in `I minus {b_0}` whose
product `P_0` is divisible by `prod(A_0)`.  Write

\[
                       P_0=\prod(A_0)c,\qquad b_0=Md.
\]

The ten points obtained by adjoining `b_0` are distinct, and their product is

\[
                       P_0b_0=M\prod(A_0)cd,
\]

which is divisible by `prod(A)`.  This completes the aligned case without
reusing any prime-power contribution from `b_0`.

## Audit status

The original frozen Section 8 has a genuine logical gap.  The replacement
above is a complete proposed repair.  Its new finite robustness claims are
independently exhausted by `erdos708_c10_aligned_repair_audit.py`; the written
argument, rather than the bounded arithmetic checks, covers arbitrary scales
and valuations.
