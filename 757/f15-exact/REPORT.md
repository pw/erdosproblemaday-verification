# Erdős problem #757 — wave 7k

Date: 2026-08-12 (UTC; original report accessed 2026-07-27)

## Claim labels

- **(a) elementary-rigorous**: proved below from definitions.
- **(b) rigorous-modulo-named-theorem**: the deduction is complete, conditional only on the explicitly named published theorem.
- **(c) plausible/structural-unverified**: heuristic only. No result below rests on a claim of this type.
- **(d) computational-only**: finite exhaustive exact-arithmetic calculation, reproducible by the standalone checker.

## Step 0: authoritative live-page gate

I read the live problem page and its full discussion thread through the Bright
Data browser path, not through datacenter `curl`. The page loaded successfully.

### Verbatim live statement

> Let $A\subset \mathbb{R}$ be a set of size $n$ such that every subset
> $B\subseteq A$ with $\lvert B\rvert =4$ has
> $\lvert B-B\rvert\geq 11$. Find the best constant $c>0$ such that $A$
> must always contain a Sidon set of size $\geq cn$.

This is copied verbatim from the live page's LaTeX view.

### Gate status

- Page status: **OPEN**.
- Claimed proofs: **0**.
- “Currently working on this problem”: **None**.
- “Interested in collaborating”: **None**.
- The page says it was last edited 10 April 2026.

Therefore the mandatory stop condition did not trigger.

### Live-page known results

The page states:

1. A four-element Sidon set has \(\lvert B-B\rvert=13\), so the hypothesis
   permits at most one “missing” difference. Equivalently, every four points
   determine at least five distinct (positive) distances.
2. Without loss of generality one may assume \(A\subset\mathbb N\).
3. Erdős and Sós proved \(c\geq 1/2\).
4. Gyárfás and Lehel proved
   \[
   \frac12+\frac{1}{141\cdot 76}\leq c\leq\frac35,
   \]
   with the upper construction based on the first \(n\) Fibonacci numbers.
5. Ma and Tang improved this to
   \[
   \frac9{17}\leq c\leq\frac47.
   \]

### All seven live comments

The discussion thread contains seven comments/replies and no proof claim:

1. Yongxi Lin asks whether positivity of \(A\) matters.
2. Thomas Bloom replies that translation removes the issue and that one may
   even assume \(A\subset\mathbb N\).
3. Quanyu Tang records the precise Gyárfás–Lehel bound and announces
   arXiv:2602.23282 with the \(9/17\) and \(4/7\) bounds. The comment says AI
   was used exploratorily and the arguments were subsequently human-checked.
4. Terence Tao notes that this is constant 5b in the optimization-constant
   database.
5. Nat Sothanaphan posts “Congrats.”
6. Nat Sothanaphan posts that a standard GPT check found no issue.
7. Quanyu Tang replies “Thanks!”

The site itself warns that comments are user-supplied and unverified. Nothing
in them indicates a current worker, claimed proof, solution, or falsification.

Live sources:

- [Problem #757](https://www.erdosproblems.com/757)
- [Full discussion thread](https://www.erdosproblems.com/forum/thread/757?order=oldest)
- [Live LaTeX view](https://www.erdosproblems.com/latex/757)

## Primary-source literature audit

I searched by the problem number, exact title, \((4,5)\)-set terminology, the
current rational bounds, and citations to the recent preprint.

1. **Erdős (1997).** Publisher metadata verifies P. Erdős, “Some old and new
   problems in various branches of combinatorics,” *Discrete Mathematics*
   165/166 (1997), 227–231,
   [DOI 10.1016/S0012-365X(96)00173-2](https://doi.org/10.1016/S0012-365X(96)00173-2).
   The full text was not openly exposed by the publisher in this run.
   Ma–Tang explicitly locate this problem on p. 231. There is also a different,
   much older Erdős paper with nearly the same title; I did not conflate it
   with this source.
2. **Gyárfás–Lehel (1995).** The publisher abstract verifies the definition,
   the linear-size Sidon-subset problem, a lower bound
   \((1/2+\varepsilon)n\), and an upper bound \(3n/5+1\):
   A. Gyárfás and J. Lehel, “Linear Sets with Five Distinct Differences among
   Any Four Elements,” *J. Combin. Theory Ser. B* 64 (1995), 108–118,
   [DOI 10.1006/jctb.1995.1028](https://doi.org/10.1006/jctb.1995.1028).
   The exact displayed \(\varepsilon=1/(141\cdot76)\) was checked against both
   the authoritative live page and the Ma–Tang source.
3. **Henning–Yeo (2021).** The publisher abstract explicitly states that a
   3-uniform linear hypergraph avoiding the affine-plane-minus-two-vertices
   configuration satisfies
   \[
   17\tau(H)\leq 5n_H+3m_H.
   \]
   See M. A. Henning and A. Yeo, “Affine Planes and Transversals in
   3-Uniform Linear Hypergraphs,” *Graphs and Combinatorics* 37 (2021),
   867–890,
   [DOI 10.1007/s00373-021-02285-x](https://doi.org/10.1007/s00373-021-02285-x).
4. **Ma–Tang (2026).** I downloaded and read the current v2 TeX source, not
   only its abstract: J. Ma and Q. Tang, “Largest Sidon subsets in weak Sidon
   sets,” [arXiv:2602.23282v2](https://arxiv.org/abs/2602.23282v2), updated
   6 March 2026. It proves the limit/infimum characterization, records the
   AP-hypergraph reduction and the \(F_7\)-free input, applies the
   Henning–Yeo theorem, and gives the 14-point block
   \[
   A_{14}=\{0,136,200,243,246,249,272,286,298,323,400,528,596,1056\}
   \]
   with \(h(A_{14})=8\). Their independent code repository is
   [ep757-45set-base-block-verification](https://github.com/QuanyuTang/ep757-45set-base-block-verification).

Targeted searches found no later primary paper improving the Ma–Tang interval.
This is a search result, not a proof that no such paper exists. The live page
and the current optimization-constant database also still display
\([9/17,4/7]\).

## Setup

For a finite set \(A\), let \(h(A)\) be the largest size of a Sidon subset,
where “Sidon” means that all sums \(x+y\), \(x\leq y\), are distinct. Define
\[
f(n)=\min\{h(A): |A|=n,\ A\text{ is a }(4,5)\text{-set}\}.
\]
Ma–Tang prove
\[
c_*=\lim_{n\to\infty}\frac{f(n)}n
    =\inf_{n\geq1}\frac{f(n)}n.
\]

For sorted \(A=\{a_0<\cdots<a_{n-1}\}\), its AP hypergraph \(H(A)\) has vertex
set \(A\) and an edge \(\{a_i,a_j,a_k\}\) exactly when
\(a_i+a_k=2a_j\).

## An exact elementary characterization

### Lemma 1 — four-gap characterization **(a)**

A finite real set \(A\) is a \((4,5)\)-set if and only if:

1. \(A\) is weak Sidon (all sums of two *distinct* elements are distinct), and
2. its AP hypergraph \(H(A)\) is linear (two edges meet in at most one vertex).

#### Proof

Take a sorted quadruple \(x_0<x_1<x_2<x_3\) and put
\[
p=x_1-x_0,\qquad q=x_2-x_1,\qquad r=x_3-x_2.
\]
Its six positive distances are
\[
p,\ q,\ r,\ p+q,\ q+r,\ p+q+r.
\]
Apart from impossible comparisons with a strictly larger positive sum, the
only possible equalities are
\[
p=q,\quad q=r,\quad r=p+q,\quad p=q+r,\quad p=r.
\]
The first four say, respectively, that one of the four triples in the
quadruple is a three-term AP. The last equality \(p=r\) is exactly
\[
x_0+x_3=x_1+x_2,
\]
a weak-Sidon violation; it also forces \(p+q=q+r\), so the quadruple then has
at most four distinct distances.

Thus weak Sidonicity rules out \(p=r\). Subject to that, at least five
distances occur exactly when the quadruple contains at most one AP triple.
Two distinct triples inside one quadruple share two vertices, so “at most one
AP triple in every quadruple” is exactly linearity of \(H(A)\). This proves
both directions. \(\square\)

### Lemma 2 — Sidon subsets are independent sets **(a)**

If \(A\) is weak Sidon, then \(S\subseteq A\) is Sidon if and only if \(S\)
contains no three-term AP. Hence
\[
h(A)=\alpha(H(A)).
\]

Indeed, an AP \(x-d,x,x+d\) gives
\((x-d)+(x+d)=x+x\). Conversely, a repeated Sidon sum cannot use four
distinct elements because \(A\) is weak Sidon; with three distinct values it
must have the form \(u+w=2v\).

### Lemma 3 — the midpoint bound **(a)**

For a weak Sidon set of size \(n\geq2\), distinct AP edges have distinct
midpoints. Otherwise two different endpoint pairs have the same sum \(2a_j\).
The minimum and maximum elements cannot be midpoints, so
\[
m(H(A))\leq n-2.
\]

These lemmas are proved here rather than imported. The additional fact that
\(H(A)\) is \(F_7\)-free is the named Gyárfás–Lehel result used by Ma–Tang,
where
\[
E(F_7)=\{012,034,056,135,246\}.
\]

## A finite-size sharpening hidden in the current proof

Henning–Yeo, applied exactly as in Ma–Tang, gives **(b)**
\[
17\tau(H(A))\leq5n+3m.
\]
Using the *full* midpoint bound \(m\leq n-2\), without discarding its constant
term, gives
\[
17\tau(H(A))\leq 5n+3(n-2)=8n-6.
\]
Since \(\tau\) is integral and \(h(A)=\alpha(H)=n-\tau(H)\),
\[
\boxed{\quad
f(n)\geq n-\left\lfloor\frac{8n-6}{17}\right\rfloor
\quad(n\geq2).\quad} \tag{1}
\]
Ma–Tang relax \(8n-6\) to \(8n\) because they need the asymptotic constant.
Retaining \(-6\) is decisive for the small cases below.

### The exceptional \(n=5\) improvement **(a)**

Equation (1) gives only \(f(5)\geq3\), but in fact \(f(5)\geq4\).

A linear 3-graph on five vertices has at most two edges. To see this, two
edges must intersect once and together use all five vertices, say
\(\{x,a,b\}\) and \(\{x,c,d\}\). A third edge containing \(x\) cannot take
another vertex without meeting one old edge twice; a third edge not
containing \(x\) can take at most one of \(\{a,b\}\) and at most one of
\(\{c,d\}\), so it cannot have three vertices.

Each 3-edge is contained in exactly two of the five 4-subsets. Two edges
therefore cover at most four 4-subsets, leaving a 4-subset with no AP.
Lemma 2 makes that subset Sidon.

## Explicit 12-point block found in this run

The capped construction search found
\[
\boxed{
A_{12}=\{0,97,161,194,227,322,374,454,521,534,547,720\}.
}
\]

I do not claim priority for the mere existence of a 12-point \(h=7\) block:
Ma–Tang's AI-usage declaration says their exploration first found a 12-point
example before the published 14-point block, but their paper and verification
repository do not give that earlier block's coordinates. The set above is an
explicit, independently checkable instance produced in this run.

Its complete AP edge list, in zero-based indices, is
\[
\begin{aligned}
&(0,1,3),(0,2,5),(0,4,7),(1,5,10),(2,3,4),\\
&(4,6,8),(5,8,11),(6,7,9),(6,10,11),(8,9,10).
\end{aligned}
\]

The dependency-free checker verifies **(d)**:

- all \(\binom{12}{4}=495\) quadruples have at least five distinct distances;
- the minimum attained number is exactly five;
- all 66 sums of distinct pairs are different;
- the AP list above is complete and linear;
- every subset of size \(8,9,10,11,\) or \(12\) is non-Sidon
  (794 subsets in total);
- the seven-set
  \[
  \{0,97,161,227,374,534,547\}
  \]
  is Sidon.

Consequently
\[
h(A_{12})=7.
\]

The discovery model used ordered integer variables \(0=a_0<\cdots<a_{11}\leq
5000\), exact AP indicator variables, an all-different constraint on sums of
distinct pairs, at most one AP in every 4-set, and at least one AP in every
8-set. It required ten AP edges. The successful capped run took under 40
seconds wall time. The result does not depend on that solver: the standalone
verification is an exhaustive exact-integer calculation using only Python's
standard library.

This \(7/12\) ratio does not improve the current asymptotic upper bound
\(4/7\); its value here is that it closes the lone gap in the explicit
finite-order table.

## Exact 15-point extension found in the update

Adjoin 1057 to Ma--Tang's 14-point block:
\[
\boxed{
A_{15}=\{0,136,200,243,246,249,272,286,298,323,400,528,596,1056,1057\}.
}
\]

The updated dependency-free checker verifies directly from the live
definitions **(d)**:

- all \(\binom{15}{4}=1365\) quadruples have \(|B-B|\ge11\): the exact
  histogram is 144 quadruples with 11 signed differences and 1221 with 13;
- all 105 sums of distinct pairs are different;
- the AP hypergraph has the same twelve edges as the 14-point block, so 1057
  lies in no AP and the hypergraph remains linear;
- every one of the \(2^{15}=32768\) subsets passes through the direct Sidon
  predicate; there are 143 Sidon nine-subsets and none of size at least ten;
- in particular, all \(\binom{15}{10}=3003\) ten-subsets are non-Sidon, while
  \[
  \{0,136,200,243,246,298,323,528,1057\}
  \]
  is Sidon.

Thus \(h(A_{15})=9\). On the other hand, (1) gives **(b)**
\[
f(15)\ge15-\left\lfloor\frac{8\cdot15-6}{17}\right\rfloor
=15-6=9.
\]
Therefore
\[
\boxed{f(15)=9.}
\]

An independent second checker evaluates the literal \(|B-B|\) predicate and
the critical 10- and 9-subset layers via both the sum definition and the
positive-distance formulation.

The 2026-08-12 live discussion still had seven comments and none mentioned
this finite extension. The current Ma--Tang v2 TeX and companion repository
contain the 14-point block but no `1057`, `f(15)`, or 15-point construction.
This targeted miss is evidence about novelty, not a proof of priority.

## Exact table through \(n=15\)

Here are explicit extremal sets used by the checker:

```text
n= 1: {0}
n= 2: {0,97}
n= 3: {0,97,194}
n= 4: {0,97,161,194}
n= 5: {0,97,161,194,227}
n= 6: {0,97,161,194,227,322}
n= 7: {0,97,161,194,227,322,374}
n= 8: {0,97,161,194,227,322,454,547}
n= 9: {0,97,161,194,227,322,374,454,534}
n=10: {200,243,246,249,272,286,298,323,400,528}
n=11: {0,97,161,194,227,322,374,454,521,534,547}
n=12: {0,97,161,194,227,322,374,454,521,534,547,720}
n=13: {0,136,200,243,246,249,272,286,298,323,400,528,596}
n=14: {0,136,200,243,246,249,272,286,298,323,400,528,596,1056}
n=15: {0,136,200,243,246,249,272,286,298,323,400,528,596,1056,1057}
```

The \(n=10,13,14\) sets are subsets of the Ma–Tang 14-point block, the
15-point set is its new one-point extension, and the rest are subsets of the
new 12-point block. The checker tests every construction directly.

Combining (1), the elementary \(n=5\) argument, and the exact construction
checks gives:

| \(n\) | lower bound from (1) | final lower bound | checked \(h(A_n)\) | exact \(f(n)\) |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 |
| 3 | 2 | 2 | 2 | 2 |
| 4 | 3 | 3 | 3 | 3 |
| 5 | 3 | 4 (elementary patch) | 4 | 4 |
| 6 | 4 | 4 | 4 | 4 |
| 7 | 5 | 5 | 5 | 5 |
| 8 | 5 | 5 | 5 | 5 |
| 9 | 6 | 6 | 6 | 6 |
| 10 | 6 | 6 | 6 | 6 |
| 11 | 7 | 7 | 7 | 7 |
| 12 | 7 | 7 | 7 | 7 |
| 13 | 8 | 8 | 8 | 8 |
| 14 | 8 | 8 | 8 | 8 |
| 15 | 9 | 9 | 9 | 9 |

Thus **(b)+(d)**
\[
\boxed{
(f(1),\ldots,f(15))
=(1,2,2,3,4,4,5,5,6,6,7,7,8,8,9).
}
\]
The lower half is rigorous modulo the named Gyárfás–Lehel \(F_7\)-freeness
and Henning–Yeo transversal theorem (except the elementary \(n=5\) patch);
the matching upper half is finite exhaustive computation.

## Independent from-scratch \(n=7\) audit

As a check not using Henning–Yeo or \(F_7\)-freeness, the verifier completely
enumerates the \(n=7\) obstruction **(d)**.

If \(h(A)\leq4\), every five vertices of \(H(A)\) contain an edge. Midpoint
injectivity allows at most one edge with each midpoint index \(j=1,\ldots,5\).
The number of labelled choices, including “no edge” at a midpoint, is
\[
\prod_{j=1}^{5}\bigl(1+j(6-j)\bigr)
=6\cdot9\cdot10\cdot9\cdot6
=29160.
\]
Exact enumeration gives:

- 2,364 linear candidates;
- 48 linear candidates with independence number at most 4;
- every one of those 48 has five AP equations of exact rational rank 5;
- after normalizing \(a_0=0,a_6=1\), only four solutions are strictly
  increasing.

The four normalized solutions and a forced weak-Sidon collision are:

| normalized coordinates | collision |
|---|---|
| \((0,\frac15,\frac3{10},\frac25,\frac12,\frac35,1)\) | \(a_0+a_4=a_1+a_2=\frac12\) |
| \((0,\frac14,\frac38,\frac12,\frac58,\frac34,1)\) | \(a_0+a_4=a_1+a_2=\frac58\) |
| \((0,\frac3{10},\frac25,\frac12,\frac35,\frac7{10},1)\) | \(a_0+a_5=a_1+a_2=\frac7{10}\) |
| \((0,\frac25,\frac12,\frac35,\frac7{10},\frac45,1)\) | \(a_0+a_6=a_1+a_3=1\) |

So no seven-point \((4,5)\)-set has \(h\leq4\). This independently confirms
\(f(7)\geq5\), while the displayed seven-point construction gives equality.
All equation solving uses `fractions.Fraction`; there is no floating point.

## Reproduction

Run:

```bash
python runs/erdos757_wave7k_reverify.py
python runs/erdos757_wave7k_a15_audit.py
```

The frozen publication bundle, including both checkers and recorded outputs,
is in the
[`verification/757/f15-exact`](https://github.com/pw/ErdosProblemADay.com/tree/main/verification/757/f15-exact)
directory of the site repository.

The standalone file is
[`runs/erdos757_wave7k_reverify.py`](erdos757_wave7k_reverify.py). It has no
third-party dependencies. On this VM it completes in about 0.06 seconds and
ends with:

```text
PASS: all construction, table, arithmetic, and n=7 checks succeeded
```

The independent 15-point audit is
[`runs/erdos757_wave7k_a15_audit.py`](erdos757_wave7k_a15_audit.py). It
implements the live difference-set predicate and the critical Sidon checks
separately from the integrated checker.

The program recomputes rather than embeds:

1. every pair sum used in each Sidon test;
2. every distance in every four-subset, including all 1365 at order 15;
3. every largest-Sidon-subset value, including all 32768 subsets of \(A_{15}\);
4. the complete AP list of \(A_{12}\);
5. every floor and integer inequality in (1);
6. all 29,160 midpoint-labelled seven-point AP patterns; and
7. all rational ranks, normalized solutions, and weak-Sidon collisions.

## What remains and the precise wall

This does **not** determine \(c_*\) and does not improve the current uniform
interval
\[
\frac9{17}\leq c_*\leq\frac47.
\]
Finite values through 15 do not supply the missing asymptotic uniformity.

There are two concrete next targets:

1. **Upper-bound target.** By Ma–Tang's
   \(c_*=\inf_n f(n)/n\), one finite block with
   \(h(A)/|A|<4/7\) improves the upper bound. Bound (1) rules out such a block
   at \(n=15\): the new construction attains its forced value \(h=9\), while
   strict asymptotic improvement would need \(h\leq8\). The first numerically
   possible order is \(n=16\), where a
   16-point \((4,5)\)-set with \(h=9\) would give
   \[
   c_*\leq\frac9{16}<\frac47.
   \]
   A direct integer model at \(n=16\) has 560 AP indicators, 120
   distinct-pair sums, 1,820 four-set linearity constraints, and 8,008
   ten-set covering constraints. A bounded-span pilot should be budgeted at
   roughly 1–10 core-hours; several bounds/seeds or a certificate-quality
   sweep would plausibly cost tens of core-hours. Such a bounded integer
   miss would still not prove nonexistence over all reals.
2. **Lower-bound target.** The exact missing lemma is a stronger transversal
   inequality for *ordered, arithmetically realizable* AP hypergraphs, beyond
   the general
   \[
   \tau(H)\leq\frac{8}{17}|V(H)|+O(1).
   \]
   To meet the existing \(4/7\) upper bound one would need, at minimum,
   \[
   \tau(H(A))\leq\frac37|A|+o(|A|)
   \quad\text{or equivalently}\quad
   \alpha(H(A))\geq\frac47|A|-o(|A|).
   \]
   Linearity, midpoint injectivity, and \(F_7\)-freeness alone currently give
   only the Henning–Yeo coefficient. What is missing is an inequality that
   exploits the simultaneous ordered equations
   \(a_i+a_k=2a_j\), not merely the abstract hypergraph.

No conjectural extrapolation of the small table is used as a theorem.

PARTIAL: Exact finite result \(f(1),\ldots,f(15)=(1,2,2,3,4,4,5,5,6,6,7,7,8,8,9)\), with explicit 12-point and 15-point blocks and dependency-free exhaustive checkers; the asymptotic constant remains \(9/17\le c_*\le4/7\).
