# Erdős problem 352 — wave w041

Date: 2026-08-12 (UTC; initial run 2026-07-31)

## Claim labels

- **[a] elementary-rigorous:** a complete non-computational argument is given
  here.
- **[b] rigorous modulo named theorem/source:** the theorem and primary source
  are identified.
- **[c] plausible/structural-unverified:** explicitly not asserted as a
  theorem.
- **[d] computational-only:** a finite exact computation with a standalone
  checker.
- **[source-checked]:** a bibliographic or live-site fact directly checked at
  the linked source; this is not a mathematical-proof label.

## 2026-08-12 second update: the exact value `f(18)=34`

The finite computation has now been extended by one further exact value:

\[
                              \boxed{f(18)=34}.                 \tag{V1}
\]

This is **[d: computational-only]** and still does not prove the uniform
estimate `f(N)=O(N)` needed for the continuous problem.

The 34-point lower witness was posted previously and is frozen in the public
witness repository cited below. The independent audit checks all
\(\binom{34+2}{3}=7{,}140\) triples with repetition using

\[
                 (A_2-36)^2-4D_2>0.                            \tag{V2}
\]

All pass; the minimum integer margin is 21. No priority claim is made for the
witness. **[d, source-checked]**

For the upper bound, the exhaustive diameter-pair reduction has 140
normalized vectors, 140 no-high branches, and 12,594 fixed-high branches.
The primary audit reconstructs 12,734 coloring certificates and directly
checks 3,011,741 same-color pairs. Pair coloring bounds every branch by 34
except the no-high branch with `B=(5,4)`, where its relaxation gives 35.
**[d]**

That exceptional branch has 42 low candidates and 57 incompatibility edges.
The following nine edges form a matching:

```text
(-1,2)--(6,2)    (-1,3)--(2,-1)   (0,1)--(3,-2)
(0,4)--(3,-1)    (1,-1)--(4,5)    (1,5)--(4,-1)
(2,5)--(5,0)     (2,6)--(5,3)     (3,5)--(6,1)
```

If 33 candidates were pairwise compatible, their nine omitted vertices would
be a vertex cover and would have to select exactly one endpoint from each
matching edge. An exhaustive audit of all `2^9=512` endpoint choices finds
exactly two vertex covers. The first surviving 33-set contains both forbidden
triples

```text
(1,-1), (1,4), (6,1)
(1,-1), (1,4), (6,2),
```

and the second contains both

```text
(-1,2), (4,0), (4,5)
(-1,3), (4,0), (4,5).
```

Each has `A_2=25`, `D_2=34`, and exact margin

\[
                         (25-36)^2-4\cdot34=-15.              \tag{V3}
\]

Thus the exceptional branch has at most 32 candidates, hence at most 34
points after restoring its diameter pair. This closes the upper half of
(V1). **[d]**

The complete run took 216.13 seconds and 20,940 KiB maximum resident memory.
Its canonical audited certificate-stream SHA-256 is
`b761add523bbe8a4f1d8f822268ddc28a893e9a1318ebc73807822d7ca09fea8`.
A separate focused checker rebuilds the witness, lens, incompatibility graph,
matching, covers, and four failed triples directly in under a second. The
versioned verification bundle is
[`verification/352/f18-exact`](https://github.com/pw/ErdosProblemADay.com/tree/main/verification/352/f18-exact).
Run the assertion-based checker with ordinary `python3`, never `python3 -O`.
**[d]**

## 2026-08-12 first update: the exact value `f(17)=32`

The live problem, discussion, and proof-claim pages were fetched again through
the Bright Data browser before this update. They still showed status **OPEN**,
17 comments, **0 claimed proofs**, and **Currently working on this problem:
None**. The dedicated proof page again said that no proof claims had been
submitted. **[source-checked]**

The finite computation below has now been extended by one exact value:

\[
                              \boxed{f(17)=32}.                 \tag{U1}
\]

This is **[d: computational-only]**. It does not prove the uniform estimate
`f(N)=O(N)` and therefore does not solve the continuous problem.

The 32-point lower witness was posted previously by BorisAlexeev and appears
in KentaKitamura's public witness repository. An independent definition-level
check evaluates all
\(\binom{32+2}{3}=5{,}984\) triples with repetition using the exact predicate

\[
                 (A_2-34)^2-4D_2>0.                            \tag{U2}
\]

All pass, and the minimum integer margin is 5. No priority claim is made for
this witness. **[d, source-checked]**

For the upper bound, the same diameter-pair reduction described below gives
125 normalized vectors `B`, 125 no-high branches, and 9,414 fixed-high
branches. Deterministic proper colorings, independently audited by full triple
enumeration within every color class, bound every branch by 32 except the
no-high branch with `B=(5,4)`. Across all 9,539 branches the audit checks
1,534,917 same-color pairs. **[d]**

The exceptional branch has 40 low candidates and an incompatibility graph
with 48 edges. It contains the following matching of nine disjoint edges:

```text
(-1,2)--(4,0)    (-1,3)--(3,0)    (0,3)--(4,-1)
(0,4)--(2,-1)    (1,-1)--(4,5)    (1,4)--(6,1)
(1,5)--(5,1)     (2,5)--(5,0)     (3,5)--(6,2)
```

A pairwise-compatible 31-subset would have to omit exactly one endpoint of
each matching edge. The checker audits all `2^9=512` choices. Exactly two
nine-point omissions cover all 48 incompatibility edges. The corresponding
31-subsets are respectively killed by the triples

```text
(0,3), (3,-1), (4,5)
(1,-1), (2,5), (5,1).
```

For each triple, `A_2=22` and `D_2=37`, so its exact margin is

\[
                         (22-34)^2-4\cdot37=-4.                \tag{U3}
\]

Thus the exceptional branch contains at most 30 candidates, or 32 points
after adjoining its diameter pair. This proves the upper half of (U1). **[d]**

Two standalone implementations and their logs are frozen in the versioned
[verification bundle](https://github.com/pw/ErdosProblemADay.com/tree/main/verification/352/f17-exact).
The primary checker reconstructs every branch and prints certificate-stream
SHA-256
`dd1b957a56174169a95cc31fd68d77b47d51dd38745f6252059954b74aad78e2`.
A hostile implementation uses a different shoelace/dot-product geometry path
and set-based DSATUR coloring; it independently reproduces the global cap and
all branch counts. A separate 80-decimal radical audit checks 5,984 witness
triples and 21,119 lens triples. It finds 12 exact zero-margin lens triples,
so the strict sign in (U2) is materially exercised rather than vacuous.
**[d]**

The full primary run took 113.40 seconds and 20,292 KiB maximum resident
memory; the independent full branch audit took 211.23 seconds and 19,428 KiB.
The short matching audit takes under a second. Run the assertion-based
checkers with ordinary `python3`, never `python3 -O`. **[d]**

## Initial 2026-07-31 live-page check

I fetched the live
[problem page](https://www.erdosproblems.com/352), its complete
[discussion thread](https://www.erdosproblems.com/forum/discuss/352), and its
[proof-claim page](https://www.erdosproblems.com/forum/thread/352/proof-claims)
through the Bright Data browser on 2026-07-31. Direct extraction was allowed to
finish before any mathematical work. **[source-checked]**

The live statement, verbatim apart from normalizing its visual line breaks, is:

> Is there some 𝑐 >0 such that every measurable 𝐴 ⊆ℝ² of measure ≥𝑐 contains
> the vertices of a triangle of area 1?

The same page displayed all of the following:

- status: **OPEN**;
- last edited: **23 January 2026**;
- **17 comments on this problem**;
- **0 claimed proofs for this problem**; the dedicated page says “No proof
  claims have been submitted yet”;
- **Currently working on this problem: None**;
- **Interested in collaborating: Vjeko_Kovac, JineonBaek,
  J_Koizumi_144**.

Thus neither mandatory stop condition applied. In particular, “interested in
collaborating” is recorded but is not the page's “currently working” marker.
**[source-checked]**

### Known results displayed on the live page

The page lists the following facts.

1. Erdős proved (unpublished) that an infinite-measure planar set, or an
   unbounded positive-measure set, contains a triangle of every prescribed
   positive area. The cited Erdős sources say this follows easily from the
   Lebesgue density theorem. **[b, source-checked]**
2. Erdős suggested the sharp constant
   \[
                         c_0=\frac{4\pi}{\sqrt{27}}\approx2.418.
   \]
   An open disk of radius \(<2\cdot3^{-3/4}\) is the obstruction: its largest
   inscribed triangle is equilateral and has area \(<1\). **[a for the disk
   calculation; source-checked for Erdős's conjecture]**
3. Freiling and Mauldin proved that outer measure \(>c_0\) forces a triangle
   of area \(>1\). The page notes that this gives the original threshold for a
   compact convex set. **[b: Mauldin 2002, source-checked]**
4. It suffices to settle the question for sets that are unions of the
   interiors of finitely many compact convex sets; Freiling and Mauldin proved
   the sharp \(c_0\) result for unions of at most three such sets.
   **[b: Mauldin 2013, source-checked]**

### What the 17 live comments add

The site warns that comments are user-supplied and not verified. I read all 17
and used them only after the checks described below. **[source-checked]**

- The comments supply the older Erdős references and the Mauldin 2002/2013
  references, now incorporated into the main page.
- J_Koizumi_144 gives a precise lattice reduction. A finite
  \(S\subset\mathbb Z^2\) is called \(N\)-avoiding when
  \[
       \bigl|\operatorname{area}(\triangle pqr)-N\bigr|
              >\operatorname{diam}(\triangle pqr)             \tag{1}
  \]
  for every triple \(p,q,r\in S\), with repetitions allowed. If \(f(N)\) is
  the maximum size of such a set, the continuous problem is equivalent to
  \(f(N)=O(N)\). A linked note contains the proof.
- BorisAlexeev posted candidate lower-bound witnesses through \(N=27\).
  KentaKitamura's public repository rechecks those and supplies additional
  witnesses through \(N=40\).
- KentaKitamura posted a diameter-pair/compatibility-graph upper-bound scheme
  and exact values only for \(N=1,\ldots,7\):
  \[
                        1,4,4,7,9,10,12.
  \]
  The comment says the readable exact-chromatic implementation became too
  slow beyond \(7\).
- A separate comment claims and argues that the all-low subproblem has sharp
  asymptotic
  \((4\pi/\sqrt{27})N+O(\sqrt N)\). Other comments discuss dyadic
  discretization, horizontal sections, toy grid computations, disk-like
  extremizers, and widely separated “local extremizers.” These are useful
  structural context, not claimed proofs of the full problem.
- The newest substantive continuous result cited in the thread is the May
  2026 preprint of Bulj and Kovač discussed below.

All names, dates, links, tables, and the previous \(N\le7\) exact range in
this inventory were checked in the rendered thread. **[source-checked]**

## Primary-source literature audit

1. Paul Erdős, *Set-theoretic, measure-theoretic, combinatorial, and
   number-theoretic problems concerning point sets in Euclidean space*, Real
   Analysis Exchange 4 (1978/79), 113–138,
   [author archive PDF](https://www.renyi.hu/~p_erdos/1978-40.pdf).
   Pages 121–123 state the infinite-measure observation, the finite constant
   question, the disk obstruction, and the proposed value
   \(4\pi/\sqrt{27}\). **[b, source-checked]**

2. R. Daniel Mauldin, *Some Problems in Set Theory, Analysis and Geometry*,
   in *Paul Erdős and His Mathematics I*, Bolyai Society Mathematical Studies
   11 (2002), 493–506,
   [author-uploaded PDF](https://www.researchgate.net/profile/R-Mauldin-2/publication/2363356_Some_Problems_in_Set_Theory_Analysis_and_Geometry/links/0c96052951f2fa7f84000000/Some-Problems-in-Set-Theory-Analysis-and-Geometry.pdf).
   Section 1 states the Freiling–Mauldin outer-measure theorem and the
   convex/covering reductions used on the live page. **[b, source-checked]**

3. R. Daniel Mauldin, *Some Problems and Ideas of Erdős in Analysis and
   Geometry*, in *Erdős Centennial* (2013), 365–376,
   [author-hosted PDF](https://sites.math.unt.edu/~mauldin/papers/no153.pdf),
   [DOI](https://doi.org/10.1007/978-3-642-39286-3_13).
   Problems 5.1 and 5.2 give the continuous problem and finite-union reduction;
   the following paragraphs prove the sharp constant for one, two, and three
   compact convex bodies. **[b, source-checked]**

4. J. Koizumi, *Triangles in a Planar Measurable Set*,
   [linked note](https://jkoizumi144.com/notes/erdos352.pdf).
   Theorem 2 states and proves the equivalence with \(f(N)=O(N)\). This is an
   informal linked note rather than a journal publication, so I independently
   reconstruct the reduction below. **[source-checked; mathematical use is
   [a]]**

5. Aleksandar Bulj and Vjekoslav Kovač, *On hyperbolic corners and unit-area
   triangles in planar sets of large measure*,
   [arXiv:2605.30033v1](https://arxiv.org/abs/2605.30033), submitted 28 May
   2026. The identifier, title, authors, date, and full 25-page paper all
   exist. Its Theorem 2 says that if \(M_\triangle(R)\) is the supremum of
   measures of unit-area-triangle-avoiding measurable subsets of
   \([0,R]^2\), then for \(R\ge10\)
   \[
       M_\triangle(R)\lesssim
       R^2\left(\frac{\log\log R}{\log R}\right)^{1/2}.        \tag{2}
   \]
   The paper explicitly says the desired \(O(1)\) bound remains open.
   **[b, source-checked]**

Targeted searches for the exact statement, “triangle of area one,”
“unit-area triangles” with measurable sets, Freiling–Mauldin, and “Erdős
Problem #352” found no later primary source claiming the full problem or the
exact lattice values below. This is a search miss and not a proof of novelty.
**[c, source-checked]**

## Initial finite result through `N=16`

Let \(f(N)\) have the precise meaning in (1).

### Theorem

The exact values for \(8\le N\le16\) are
\[
\begin{array}{c|rrrrrrrrr}
N    &8&9&10&11&12&13&14&15&16\\ \hline
f(N) &14&16&18&21&23&24&26&28&32.
\end{array}                                                    \tag{3}
\]
**[d: exhaustive integer certificates]**

The lower-bound point sets were already present in the live thread/witness
repository; this run independently verifies them. The new contribution of
this run is the matching exhaustive upper bound for every \(N=8,\ldots,16\).
Thus it extends the posted exact range \(N\le7\), but it does not give a new
continuous counterexample or solve the uniform problem. **[d,
source-checked]**

The July run's standalone checker was
`runs/erdos352_wavew041_reverify.py`. It used only the Python standard
library, embedded every lower witness, constructed every upper certificate
from scratch, and then audited the certificates independently. Its SHA-256 at
the time of that initial run was

```text
3f79b4cfca1db2ada15e38ce9dac317336ae92ffb5b5a816464bd6ce41f11791
```

**[d]**

## Proof of the finite upper bounds

### 1. An exact integer predicate

For lattice points \(p,q,r\), let
\[
 A_2=\left|\det(q-p,r-p)\right|,
 \qquad
 D_2=\max\{|p-q|^2,|p-r|^2,|q-r|^2\}.
\]
Thus the triangle area is \(A_2/2\) and its diameter is \(\sqrt{D_2}\).
Both sides of (1) are nonnegative, so multiplying by two and squaring shows
that (1) is equivalent to
\[
                    (A_2-2N)^2-4D_2>0.                       \tag{4}
\]
Every comparison in the checker is therefore an exact integer comparison.
**[a]**

### 2. Exhausting diameter pairs

Repetitions in (1) matter. Applying it to \((p,p,q)\) gives
\[
                               |p-q|<N.                       \tag{5}
\]
Every finite avoiding set has a diameter pair. Translate one endpoint to
\(A=(0,0)\), and apply a sign change, coordinate swap, and reflection to put
the other endpoint at
\[
              B=(b_x,b_y),\qquad b_x\ge b_y\ge0,\quad
              0<b_x^2+b_y^2<N^2.                             \tag{6}
\]
These are all lattice-preserving isometries and preserve absolute triangle
area. The checker enumerates every vector in (6). An independent audit starts
with every signed vector in the square \([-(N-1),N-1]^2\), normalizes its full
dihedral orbit, and checks that the two lists coincide. **[a for
completeness; d for the list comparison]**

Write \(D=|A-B|\). Since \(A,B\) are a diameter pair, every further point
\(q\) lies in the finite lens
\[
                        |q-A|\le D,\qquad |q-B|\le D.          \tag{7}
\]
In particular every coordinate of \(q\) lies in
\([-(N-1),N-1]\). The checker exhausts that entire integer box, imposes (7),
and tests \((A,B,q)\) using (4). There is no truncation heuristic.
**[a,d]**

### 3. The exhaustive low/high branch split

For a surviving \(q\), the diameter of \(\triangle ABq\) is \(D\), so (1)
gives exactly one of
\[
 \operatorname{area}(\triangle ABq)<N-D
 \quad\text{or}\quad
 \operatorname{area}(\triangle ABq)>N+D.                     \tag{8}
\]
Call these candidates low and high.

Every avoiding set for a fixed \(B\) belongs to one of these exhaustive
branches:

- it contains no high point, in which case \(A,B\) are fixed and only low
  candidates remain;
- it contains a high point \(H\), in which case the checker tries every high
  candidate as \(H\) and fixes \(A,B,H\).

In either branch, candidates incompatible with the fixed points or with the
chosen diameter are first removed. **[a,d]**

### 4. Checkable colorings, not chromatic optimization

For a fixed set \(F\), where \(F=(A,B)\) or \(F=(A,B,H)\), form a graph on
the remaining candidates. Two candidates are adjacent precisely when they
can coexist with \(F\): their mutual distance does not exceed \(D\), and
every triple in \(F\cup\{p,q\}\) passes (4).

Every actual avoiding extension of \(F\) is a clique in this compatibility
graph. Consequently, any proper \(k\)-coloring—not necessarily an optimal
one—proves that at most \(k\) candidates can be added:
\[
                      |S|\le |F|+k.                           \tag{9}
\]
The program uses a deterministic degree-ordered greedy coloring. The slow
exact-chromatic search in the posted reference implementation is therefore
unnecessary for these upper bounds. **[a,d]**

The crucial certification direction is checked independently. For each color
class and every same-color pair \(p,q\), the audit verifies directly that
either \(|p-q|>D\), or a full combinations-with-repetition scan of
\(F\cup\{p,q\}\) finds a failed inequality (4). Hence no compatible pair has
the same color, which is exactly the property needed in (9). **[a,d]**

### 5. Taking all maxima

For every normalized \(B\), the checker takes the larger of the no-high bound
and all fixed-\(H\) bounds. It then takes the maximum over all \(B\).
Sections 2–4 show that every \(N\)-avoiding lattice set occurs in one of the
audited cases, up to an allowed lattice isometry. The resulting upper bound
matches the embedded witness size for each row of (3), proving equality.
**[a,d]**

## Independent lower-bound and certificate audit

For a witness of size \(m\), the checker evaluates all
\(\binom{m+2}{3}\) triples with repetition. The following table records the
smallest exact value of the left side of (4), so every positive entry is a
strict certificate. It also gives the exhaustive upper-search counts.
**[d]**

| \(N\) | \(f(N)\) | witness triples | min gap | diameter \(B\) cases | high-\(H\) branches | color certificates | same-color pairs audited | tight \(B\) |
|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| 8 | 14 | 560 | 24 | 30 | 98 | 128 | 28 | \((3,3)\) |
| 9 | 16 | 816 | 29 | 38 | 268 | 306 | 50 | \((4,1),(3,3)\) |
| 10 | 18 | 1140 | 13 | 46 | 518 | 564 | 383 | \((4,3)\) |
| 11 | 21 | 1771 | 28 | 55 | 926 | 981 | 2806 | \((4,2)\) |
| 12 | 23 | 2300 | 9 | 64 | 1466 | 1530 | 10809 | \((4,4)\) |
| 13 | 24 | 2600 | 5 | 75 | 2348 | 2423 | 50654 | \((5,1),(5,2),(6,1)\) |
| 14 | 26 | 3276 | 16 | 87 | 3572 | 3659 | 148701 | \((5,2),(5,3)\) |
| 15 | 28 | 4060 | 17 | 99 | 5094 | 5193 | 373340 | \((4,4),(5,3),(5,4)\) |
| 16 | 32 | 5984 | 16 | 112 | 7094 | 7206 | 814708 | \((5,3)\) |

The script has deliberately separate producer and audit paths:

1. the producer computes area with a based-vector determinant; the audit uses
   the shoelace formula;
2. the producer computes distances from coordinate differences; the audit
   uses a dot-product expansion;
3. the producer lists normalized \(B\)'s directly; the audit normalizes every
   signed raw vector;
4. candidate pools are regenerated with the audit predicate and compared
   exactly;
5. the audit does not trust the compatibility graph: it checks every
   same-color pair by full triple enumeration and separately checks the fixed
   diameter.

Thus a search error can at worst produce a certificate that fails; no
optimizer's assertion is accepted as a proof. **[d]**

As a cross-implementation check, I also ran the public
[upper-bound repository](https://github.com/KitaKen1/erdos352-koizumi-fn-upper-bound)
at commit `7a4a19468771766cb4f20e10dfa5cf770cc2487b` with exact chromatic
minimization disabled (`--max-color-vertices 0`). Its separate implementation
returned the same upper totals and diameter-case counts for \(N=8,\ldots,16\).
The embedded lower points were compared with the public
[witness repository](https://github.com/KitaKen1/erdos352-koizumi-n-avoiding-witness-table)
at commit `09e5c5393943c881ab60118aa32fe5660539c8d5`. The standalone checker
imports neither repository. **[d, source-checked]**

For reproducibility, the SHA-256 digests of the canonical audited certificate
streams are:

```text
N= 8  82a246077f367d140d7e977167a203c15fa2fa0c3e158de41727bac94317ad41
N= 9  8c4251f00f2c14475832a7568dde89080796a126fae4a80b96a0ad549388e225
N=10  0a0c50ab0e12bca0fa487ba6f77beaaed3a64d5e78d8541f595c2d66133cbf3a
N=11  8687754c9fcf1433a3bfdc1435c3bffb1a097ae89374a44b842b209980c883c3
N=12  395fb6971b90dd2b0463323e02382890b75b4b36f91ebb621b8774e067cf2ae0
N=13  903a23b95da5c4ac678570123f410ed88138ab5fb9777bfd5244524672a52e3a
N=14  d9aa00efb67719feb1b8254925b3a321e338d52e56db068a0bfe1ae193168d9b
N=15  31650a5d06b64a1c161e117318bdab9d3103d277ab293790c27f82db7d60453f
N=16  839008d566ff41e4801c2f63fe61af5beb3081ad475a8b94864db84b7c5085d3
```

**[d]**

## Historical `N<=16` reproduction record

From the repository root:

```bash
python3 runs/erdos352_wavew041_reverify.py
```

The completed run printed:

```text
N= 8 f(N)=14 witness_triples= 560 min_gap= 24 B_cases= 30 high_branches=   98 certs=  128 same_color_pairs=    28 tight_B=3,3 sha256=82a246077f367d140d7e977167a203c15fa2fa0c3e158de41727bac94317ad41 seconds=0.053
N= 9 f(N)=16 witness_triples= 816 min_gap= 29 B_cases= 38 high_branches=  268 certs=  306 same_color_pairs=    50 tight_B=4,1;3,3 sha256=8c4251f00f2c14475832a7568dde89080796a126fae4a80b96a0ad549388e225 seconds=0.163
N=10 f(N)=18 witness_triples=1140 min_gap= 13 B_cases= 46 high_branches=  518 certs=  564 same_color_pairs=   383 tight_B=4,3 sha256=0a0c50ab0e12bca0fa487ba6f77beaaed3a64d5e78d8541f595c2d66133cbf3a seconds=0.409
N=11 f(N)=21 witness_triples=1771 min_gap= 28 B_cases= 55 high_branches=  926 certs=  981 same_color_pairs=  2806 tight_B=4,2 sha256=8687754c9fcf1433a3bfdc1435c3bffb1a097ae89374a44b842b209980c883c3 seconds=1.045
N=12 f(N)=23 witness_triples=2300 min_gap=  9 B_cases= 64 high_branches= 1466 certs= 1530 same_color_pairs= 10809 tight_B=4,4 sha256=395fb6971b90dd2b0463323e02382890b75b4b36f91ebb621b8774e067cf2ae0 seconds=2.363
N=13 f(N)=24 witness_triples=2600 min_gap=  5 B_cases= 75 high_branches= 2348 certs= 2423 same_color_pairs= 50654 tight_B=5,1;5,2;6,1 sha256=903a23b95da5c4ac678570123f410ed88138ab5fb9777bfd5244524672a52e3a seconds=6.082
N=14 f(N)=26 witness_triples=3276 min_gap= 16 B_cases= 87 high_branches= 3572 certs= 3659 same_color_pairs=148701 tight_B=5,2;5,3 sha256=d9aa00efb67719feb1b8254925b3a321e338d52e56db068a0bfe1ae193168d9b seconds=13.828
N=15 f(N)=28 witness_triples=4060 min_gap= 17 B_cases= 99 high_branches= 5094 certs= 5193 same_color_pairs=373340 tight_B=4,4;5,3;5,4 sha256=31650a5d06b64a1c161e117318bdab9d3103d277ab293790c27f82db7d60453f seconds=28.996
N=16 f(N)=32 witness_triples=5984 min_gap= 16 B_cases=112 high_branches= 7094 certs= 7206 same_color_pairs=814708 tight_B=5,3 sha256=839008d566ff41e4801c2f63fe61af5beb3081ad475a8b94864db84b7c5085d3 seconds=69.480
ALL CHECKS PASSED for N=8..16; exact table=[14, 16, 18, 21, 23, 24, 26, 28, 32]; total_seconds=122.418
```

`/usr/bin/time` independently reported 122.48 seconds elapsed, 91% CPU, and
21,796 KiB maximum resident memory. `python3 -m py_compile` also passed.
**[d]**

## Why this is relevant to the continuous problem

For completeness, here is a reconstruction of Koizumi's equivalence.

### Continuous statement implies \(f(N)=O(N)\)

Assume some constant \(c\) forces a unit-area triangle in every measurable set
of measure \(>c\). Given an \(N\)-avoiding \(S\), put a disk of radius
\(1/(3\sqrt N)\) around each \(q/\sqrt N\), \(q\in S\). The disks are disjoint
by (5).

If their union contained a unit-area triangle \(p_1p_2p_3\), set
\(q_i'=\sqrt N\,p_i\). Then
\(\operatorname{area}(\triangle q_1'q_2'q_3')=N\) and
\(|q_i-q_i'|\le1/3\). The elementary determinant perturbation bound
\[
 |\operatorname{area}(\triangle q_1q_2q_3)
   -\operatorname{area}(\triangle q_1'q_2'q_3')|
 \le 2\varepsilon\operatorname{diam}(\triangle q_1q_2q_3)
      +2\varepsilon^2
\]
with \(\varepsilon=1/3\) contradicts (1); the lattice diameter is at least
one unless all \(q_i\) coincide, and the latter is impossible because one such
small disk cannot contain a unit-area triangle. Hence the disk union avoids
unit area and
\[
                   |S|\frac{\pi}{9N}\le c,
\qquad\text{so}\qquad
                   f(N)\le\frac{9c}{\pi}N.                   \tag{10}
\]
**[a]**

### \(f(N)=O(N)\) implies the continuous statement

Conversely, assume \(f(N)\le CN\). By inner regularity, it is enough to treat
a compact \(A\) of measure \(>4\pi C\). For each integer \(N\), let \(S_N\)
contain those \(q\in\mathbb Z^2\) for which the disk of radius \(2/\sqrt N\)
about \(q/\sqrt N\) meets \(A\). These disks cover \(A\), and the sum of their
areas gives
\[
                       |S_N|\frac{4\pi}{N}>4\pi C,
\quad\text{hence}\quad |S_N|>CN\ge f(N).                     \tag{11}
\]
Thus \(S_N\) has a triple failing (1). After scaling by \(1/\sqrt N\),
its triangle area differs from \(1\) by at most its diameter divided by
\(\sqrt N\). Moving the vertex opposite a diameter side within its radius
\(2/\sqrt N\) disk changes the area continuously through an interval large
enough to hit \(1\).

This gives a unit-area triangle in the disk union for every \(N\). Each union
lies within distance \(4/\sqrt N\) of compact \(A\); compactness and area
continuity give a convergent subsequence whose limiting three vertices lie in
\(A\) and span area \(1\). Therefore the continuous problem is equivalent to
\(f(N)=O(N)\). The live page uses a threshold \(\ge c\), while the note uses
\(>c\); existence of some threshold is unchanged by increasing the constant.
**[a]**

## Exact remaining obstruction

The finite table (3) supplies no uniformity in \(N\). It therefore cannot,
even in principle, close the continuous problem. **[a]**

Within this diameter-pair method, a sufficient missing lemma is:

> There is an absolute \(C\) such that, for every \(N\), every normalized
> diameter vector \(B\), and every no-high or fixed-high branch \(F\), the
> associated compatibility graph has a proper coloring with at most
> \(CN-|F|\) colors.

Such a uniform coloring lemma would imply \(f(N)=O(N)\) by (9) and hence solve
the continuous problem by (10)–(11). The live discussion's all-low argument
does not control all fixed-high branches; those branches are the precise
remaining obstacle in this framework. **[a for the implication; c for the
prospect that such a coloring exists]**

The computational growth already shows why extending a table is not a
substitute. At \(N=17\) the full audit processed 9,414 high branches and
1,534,917 same-color pairs in 113.40 seconds. At \(N=18\) those figures rose
to 12,594 high branches and 3,011,741 same-color pairs in 216.13 seconds. No
finite extension, regardless of cost, would prove the required bound for all
\(N\). **[d]**

PARTIAL: Exact exhaustive certificates prove f(N)=14,16,18,21,23,24,26,28,32,32,34 for N=8,...,18 in Koizumi's equivalent lattice model, extending the posted exact range N<=7; Erdős problem 352 remains open because no uniform f(N)=O(N) bound is proved.
