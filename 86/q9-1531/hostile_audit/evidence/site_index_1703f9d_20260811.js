// erdosproblemaday.com — Patrick White vibe-maths his way through Erdős's
// leftover open problems, live, with an AI partner. Single-file Worker.
// Design: dark/glow "live challenge scoreboard" register (Teko/Rajdhani/
// JetBrains Mono), not academic — see feedback_swooped_by_careful_claim_posture.

const SITE = "Erdős Problem a Day";
const CREDIT_URL = "https://www.erdosproblems.com";
const VIBE_MATHING_URL = "https://pwhite.org/vibe-mathing";
const TWITTER_URL = "https://twitter.com/noself86";
import { LEDGER } from "./ledger_data.js";

// ---------------------------------------------------------------------------
// Status taxonomy. Bold badge text up front; the honest calibration note
// (what "CLOSED" does and doesn't mean yet) lives in ONE line, not a lecture.
const STATUS = {
  proof_claimed: { badge: "CLOSED", cls: "closed" },
  in_progress:   { badge: "LIVE",   cls: "live" },
  posted:        { badge: "CONFIRMED", cls: "confirmed" },
  partial:       { badge: "PARTIAL", cls: "partial" },
  refuted:       { badge: "REFUTED", cls: "refuted" },
  declined:      { badge: "NO PROOF TODAY", cls: "noproof" },
};

// ---------------------------------------------------------------------------
const entries = [
  {
    slug: "1117-maximum-modulus-points",
    problemNum: 1117,
    title: "#1117: finite-order limsup and a sharp polynomial bound",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: false,
    summary:
      "A July 2026 preprint strengthens the known affirmative limsup result " +
      "to a finite-order class-B entire function. Separately, a polynomial " +
      "whose nonzero exponents span d-m has at most d-m maximum-modulus " +
      "points on every circle, sharply. The liminf question remains open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/1117">erdosproblems.com/1117</a>,
OPEN). For an entire function f, let v<sub>f</sub>(r) count the points on
|z|=r where |f(z)| attains its maximum on that circle. Excluding monomials,
Erdős asked two different questions: can the limsup of v<sub>f</sub>(r) be
infinite, and can its liminf be infinite?</p>

<p><strong>A current literature update.</strong> The limsup half was already
answered affirmatively in 1968. A July 2026 preprint of Pardo-Simon and
Sixsmith now proves a substantially stronger version: there is a
finite-order entire function in the Eremenko-Lyubich class B and radii
r<sub>n</sub>&rarr;&infin; such that</p>

<p style="text-align:center"><strong>
v<sub>f</sub>(r<sub>n</sub>) &ge; 2n+1.
</strong></p>

<p>The quantifier matters. The construction controls selected circles. The
paper explicitly says it gives no useful control away from those radii and
that the liminf half remains open. Its separate interpolation theorem puts
prescribed points on circles of distinct radii, so it cannot be combined to
produce many points on each circle. The paper is currently an arXiv v1
preprint, not a peer-reviewed source.</p>

<p><strong>A sharp polynomial bound.</strong> There is also a clean finite
analogue. Suppose the lowest and highest nonzero powers in a non-monomial
polynomial p are m and d. Then, for every r&gt;0,</p>

<p style="text-align:center"><strong>
v<sub>p</sub>(r) &le; d-m.
</strong></p>

<p>To see it, put H(&theta;)=|p(re<sup>i&theta;</sup>)|<sup>2</sup>. The
coefficient at frequency d-m is the nonzero product of the two endpoint
coefficients, so H is a nonconstant trigonometric polynomial of exact degree
d-m. Its derivative has at most 2(d-m) zeros around the circle. If H has q
global maxima, cyclically consecutive maxima supply q distinct intervening
minima, so the derivative has at least 2q zeros. Hence q&le;d-m. The
one-maximum case uses the complementary arc from that maximum back to itself
and has a distinct interior minimum.</p>

<p>The bound is attained on every positive circle by every binomial
Az<sup>m</sup>+Bz<sup>d</sup> with AB&ne;0: equality in the triangle
inequality occurs at exactly d-m phases. We make no originality claim for
this elementary observation.</p>

<p><strong>Scope.</strong> Problem 1117 remains open in its liminf form. The
2024 approximate construction of many near-maximal arcs expressly did not
establish actual maximum points, and a fixed polynomial has a uniformly
bounded count. The verification bundle pins all three source versions,
checks the theorem's exact quantifiers, and independently audits the
polynomial proof including the cyclic one-maximum case.</p>
`,
    links: [
      { label: "erdosproblems.com/1117", url: "https://www.erdosproblems.com/1117" },
      { label: "Pardo-Simon and Sixsmith (2026)", url: "https://arxiv.org/abs/2607.09462" },
      { label: "Glucksam and Pardo-Simon (2024)", url: "https://arxiv.org/abs/2208.11154" },
      { label: "Proof, sources, and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1117/maximum-modulus-points" },
    ],
  },
  {
    slug: "149-degree4-strong-clique-20",
    problemNum: 149,
    title: "#149: the degree-4 strong clique number is 20",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: false,
    summary:
      "A July 2026 strong-clique bound, specialized at maximum degree 4, " +
      "proves the exact value 20; the C5 two-blowup attains it. This is a " +
      "literature-derived partial. The strong chromatic maximum remains " +
      "between 20 and 21, so Problem 149 is still open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/149">erdosproblems.com/149</a>,
OPEN). A strong edge coloring assigns different colors to every two edges at
distance at most two. Equivalently, it colors L(G)<sup>2</sup>. The
Erdős-Nešetřil conjecture predicts the optimal general bound; even its
maximum-degree-4 case remains unresolved.</p>

<p><strong>An exact clique result.</strong> Write</p>

<p style="text-align:center"><strong>
Omega<sub>4</sub> = max omega(L(G)<sup>2</sup>)<br>
over simple G with Delta(G)&le;4.
</strong></p>

<p>A July 2026 preprint of Kumar, Mohar, and Pragada proves the general bound</p>

<p style="text-align:center"><strong>
omega(L(G)<sup>2</sup>) &le; (2607/1987) Delta(G)<sup>2</sup>.
</strong></p>

<p>At Delta=4 the right side is 41712/1987=21-15/1987. Clique number is an
integer, so Omega<sub>4</sub>&le;20.</p>

<p>The independent two-vertex blowup of C<sub>5</sub> gives equality. It is
4-regular with 20 edges, and every two edges have line-graph distance at most
two. Thus L(G)<sup>2</sup>=K<sub>20</sub>, and</p>

<p style="text-align:center;font-size:1.1em"><strong>Omega<sub>4</sub>=20.</strong></p>

<p><strong>A disclosed source repair.</strong> The preprint is currently v1
and contains a genuine typo: an auxiliary minimum is taken over [0,1/4]
immediately after the proof shows that no value in that interval works. The
audit does not silently ignore this. It reruns the induction with the fixed
constant beta=620/1987. Exact rational expansion verifies the paper's
sum-of-a-square certificate, a negative discriminant for its remaining
quadratic, and the final induction identity. No later step uses minimality of
the malformed auxiliary quantity. The passage from the repaired bipartite
lemma to the general coefficient uses Faron and Postle's published theorem
with matching quantifiers.</p>

<p><strong>What remains open.</strong> A strong clique gives a lower bound on
the number of colors, not an upper bound. The blowup forces 20 colors, while
Huang, Santana, and Yu proved that 21 always suffice at maximum degree 4.
Therefore the exact coloring statement is still only</p>

<p style="text-align:center"><strong>20 &le; X<sub>4</sub> &le; 21.</strong></p>

<p>This is a literature-derived partial, not our discovery and not a solution
of Problem 149. The live page showed no claimed proof or current worker on 11
August 2026 and still quoted the older 4/3 strong-clique coefficient. The site
had already used the same preprint in Problem 934, but only for its separate
Section 3 L(G)<sup>3</sup> degree-diameter construction; that source overlap is
explicitly disclosed.</p>
`,
    links: [
      { label: "erdosproblems.com/149", url: "https://www.erdosproblems.com/149" },
      { label: "Kumar, Mohar, and Pragada", url: "https://arxiv.org/abs/2607.02698" },
      { label: "Faron and Postle", url: "https://arxiv.org/abs/1708.02264" },
      { label: "Proof audit and exact checkers", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/149/delta4-strong-clique-20" },
    ],
  },
  {
    slug: "196-exact-monotone-4ap-counts",
    problemNum: 196,
    title: "#196: two exact monotone 4-AP avoider counts",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "Three exact enumerations give theta_4(13)=949,812,334 and " +
      "theta_4(14)=9,471,574,188. The known table through n=12 is " +
      "independently reproduced. This is a finite counting extension only; " +
      "the singly infinite permutation problem remains open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/196">erdosproblems.com/196</a>,
OPEN). Must every permutation of the positive integers contain four values in
arithmetic progression whose positions are increasing or decreasing? The
infinite question remains open.</p>

<p><strong>A finite statistic.</strong> Let theta<sub>4</sub>(n) count
permutations of {1,...,n} with no monotone four-term arithmetic-progression
subsequence. Three complete exact enumerations now give</p>

<p style="text-align:center;font-size:1.1em"><strong>
theta<sub>4</sub>(13)=949,812,334<br>
theta<sub>4</sub>(14)=9,471,574,188.
</strong></p>

<p><strong>Prior exact data.</strong> Goh and Zhao's peer-reviewed 2021 paper
publishes an equivalent longest-progression distribution through n=10. The
public arXiv v2 table also contains rows n=11 and n=12, even though nearby
prose says the table stops at 10. Summing its columns for longest progression
lengths 1, 2, and 3 reproduces theta<sub>4</sub>(n) through n=12. The two
displayed values above are therefore the only new finite frontier claimed
here, and the dated failure to find them in prior tables is search-limited,
not an assertion of absolute priority.</p>

<p><strong>Why the computation is exact.</strong> The first program appends
unused values and rejects precisely when the new last position completes an
increasing or decreasing four-term progression; a value-complement involution
pairs its search subtrees. It was rebuilt and rerun through n=14, with a
direct all-permutations check through n=10.</p>

<p>The hostile audit then reached n=14 twice without using that search tree.
One implementation tracks progress in every oriented forbidden word and uses
no complement symmetry. Another builds every avoider by inserting the new
maximum into every possible position. Both independently return the same
9,471,574,188 count. Exhaustive Python checks through n=9, sanitizer runs,
five OpenMP thread counts, and the identity n!A<sub>4</sub>(n)/12 for total
forbidden-progression incidences supply additional controls.</p>

<p><strong>Why this does not solve Problem 196.</strong> Davis, Entringer,
Graham, and Simmons already constructed a doubly-infinite avoiding order, so
finite avoiders exist for every n without these counts. The missing step is
an avoiding order of type omega: in a singly infinite permutation every
element has only finitely many predecessors. Finite enumeration and ordinary
compactness do not provide that order-type control.</p>

<p>The live page showed no claimed proof or current worker on 11 August 2026.
The frozen package records the original computation, the corrected literature
scope, two independent n=14 enumerators, exact logs, sources, and a hostile
audit. Two non-load-bearing site snapshots were excluded because one captured
uncommitted ledger work unrelated to this problem.</p>
`,
    links: [
      { label: "erdosproblems.com/196", url: "https://www.erdosproblems.com/196" },
      { label: "Goh and Zhao", url: "https://arxiv.org/abs/2012.12339" },
      { label: "Gaiser and Horn (2026)", url: "https://arxiv.org/abs/2605.29011" },
      { label: "Exact enumerators, logs, and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/196/theta4-through-14" },
    ],
  },
  {
    slug: "213-fixed-heptagon-nonextension-96000",
    problemNum: 213,
    title: "#213: no 96,000-bounded extension of the known heptagon",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "The published diameter-22,270 integral heptagon has no distinct " +
      "eighth point whose seven distances to it are positive integers at " +
      "most 96,000. Three exact exhaustive traversals and a big-integer " +
      "metric audit certify the bounded nonextension. This concerns one " +
      "fixed heptagon and gives no lower bound for arbitrary eight-point sets.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/213">erdosproblems.com/213</a>,
OPEN). Erdős asked whether, for every n&ge;4, there are n planar points with
all pairwise distances integral, no three points collinear, and no four
concyclic. The best known construction has seven points. We do not construct
an eighth point or solve the existence problem.</p>

<p><strong>The bounded nonextension theorem.</strong> Kreisel and Kurz's
seven-point construction has diameter 22,270 and an explicit published
distance matrix. For that one fixed heptagon H, there is no distinct planar
point P such that</p>

<p style="text-align:center;font-size:1.15em"><strong>
1&le;d(P,h)&le;96,000
</strong></p>

<p>is an integer for every h&isin;H. The test imposes no general-position
condition on P: it also excludes placements that create a collinear triple or
a concyclic quadruple.</p>

<p><strong>The exact reduction.</strong> Use two heptagon vertices at distance
d=22,270 as anchors. If a candidate has integer anchor distances a and b, put</p>

<pre><code>F(d,a,b) = (d+a+b)(d+a-b)(d-a+b)(-d+a+b).</code></pre>

<p>Heron's formula makes F sixteen times the squared triangle area. A theorem
used by Kreisel and Kurz says that all nondegenerate triangles in one planar
integral point set have the same squarefree characteristic. The heptagon's
characteristic is 2,002, so every candidate not on the anchor line must obey</p>

<p style="text-align:center"><strong>F(d,a,b)=2,002s<sup>2</sup></strong></p>

<p>for an integer s. For each surviving ordered pair (a,b), the two signs of
the height give the only possible coordinates. Every remaining distance is
then checked by exact integer arithmetic after clearing the denominator
4d<sup>2</sup>. Candidates on the anchor line are enumerated separately.</p>

<p><strong>The complete search.</strong> The direct radius traversal checks
1,765,966,460 unordered strict anchor triangles. Exactly 1,017 pass the
characteristic test; restoring both anchor orders and both sides of the line
gives 4,068 coordinate candidates. Another 169,729 points cover every integer
position on the anchor line that can remain within the bound, including both
exterior endpoints at distance 96,000. None passes all seven distance tests.</p>

<p>A second implementation enumerates the same domain through Heron
semiperimeter factors and uses arbitrary-precision integers for its metric.
The hostile audit adds a third sum-and-difference traversal, regenerates the
same 1,017-row residue byte for byte, and checks all 4,068 orientations and
169,729 collinear cases with Python big integers. It also exercises all seven
coincident original vertices as required negative controls.</p>

<p><strong>What moved.</strong> The 2008 paper exhaustively searched
general-position sets of diameter at most 70,000 in a restricted
characteristic class that includes 2,002. On the overlapping general-position
extension slice for this fixed H, the checked cutoff therefore rises from
70,000 to 96,000. Our computation also covers nongeneral placements through
96,000; we do not attribute that broader coverage to the older search.</p>

<p><strong>Scope.</strong> An arbitrary eight-point configuration need not
contain a copy of this heptagon. Consequently this result does not prove that
the minimum possible eight-point diameter exceeds 96,000, does not show H is
globally inclusion-maximal, and does not settle any new cardinality in Problem
213. The live page had no claimed proof or current worker, and dated searches
found no prior fixed-H computation at this cutoff; that last statement is a
search boundary, not an absolute priority claim.</p>
`,
    links: [
      { label: "erdosproblems.com/213", url: "https://www.erdosproblems.com/213" },
      { label: "Kreisel and Kurz (2008)", url: "https://arxiv.org/abs/0804.1303" },
      { label: "OEIS A096873", url: "https://oeis.org/A096873" },
      { label: "Scanners, metric certificate, and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/213/fixed-heptagon-nonextension-96000" },
    ],
  },
  {
    slug: "1162-order-refined-p-orbit-slice",
    problemNum: 1162,
    title: "#1162: exact order counts in a p-orbit slice",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "An exact formula counts p-subgroups of S_n by order when every " +
      "nontrivial orbit has size p. One exact order already attains the " +
      "known n^2/16 leading exponent, with an explicit n log n term, and " +
      "the same restricted family has a discrete order limit law. This " +
      "refines a known construction without solving the global problem.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/1162">erdosproblems.com/1162</a>,
OPEN). Problem 1162 asks for an asymptotic formula for the number of subgroups
of the symmetric group S<sub>n</sub>, and for a statistical theorem about their
orders. Roney-Dougal and Tracey proved in 2025 that</p>

<p style="text-align:center"><strong>
|Sub(S<sub>n</sub>)|=2<sup>n&sup2;/16+o(n&sup2;)</sup>.
</strong></p>

<p>We do not solve the remaining global questions. Instead, we exactly count
by order the natural p-orbit family used in their lower-bound construction,
then extract its second-order term and its internal order distribution.</p>

<p><strong>The exact count.</strong> Fix a prime p and write n=pm+q. Let
T<sub>p</sub>(n;m,r) count the p-subgroups H&le;S<sub>n</sub> having exactly m
nontrivial orbits, each of size p, exactly q fixed points, and order p<sup>r</sup>.
If {d choose r}<sub>p</sub> denotes the Gaussian binomial coefficient, then</p>

<pre><code>T_p(n;m,r)
= n! / (q! m! [p(p-1)]^m)
  * sum_(j=0)^m (-1)^j C(m,j)
    {m-j choose r}_p.</code></pre>

<p><strong>Why the formula is exact.</strong> On each nontrivial p-point orbit,
the image of H is a regular cyclic group C<sub>p</sub>. The faithful action on
all m orbits identifies H with a vector subspace of
F<sub>p</sub><sup>m</sup> whose projection onto every coordinate is nonzero.
Inclusion-exclusion over the m coordinate hyperplanes gives the alternating
Gaussian-binomial sum.</p>

<p>The factor before the sum counts the orbit frameworks: select the fixed
points, partition the rest into unordered p-sets, and choose one regular cyclic
subgroup on each set. There is no overcount, because H itself recovers its
point-orbits and its projected cyclic group on each orbit.</p>

<p><strong>One order carries the leading exponent.</strong> At middle rank,
almost every vector subspace has full coordinate support. Combining the
Gaussian-binomial asymptotic with Stirling's formula shows that, for even n,
the single exact subgroup order 2<sup>floor(n/4)</sup> occurs</p>

<pre><code>2^(n^2/16 + (n/2)log_2(n)
   - (n/2)log_2(e) + O(1))</code></pre>

<p>times inside this family. Thus one exact order already realizes the known
n<sup>2</sup>/16 leading exponent, and this slice has an explicit positive
(n/2)log<sub>2</sub>n term. As a finite check, at n=20 the formula gives
exactly 52,502,131,339,708,050 such subgroups of order 32.</p>

<p><strong>A restricted order law.</strong> Choose uniformly from the same
p-orbit family on n=pm points, allowing every rank, and let R<sub>m</sub> be
the base-p logarithm of the subgroup order. If m=2s, then for each fixed
integer k,</p>

<p style="text-align:center"><strong>
Pr(R<sub>m</sub>&minus;s=k) &rarr;
p<sup>&minus;k&sup2;</sup> / &Sigma;<sub>j&isin;Z</sub>p<sup>&minus;j&sup2;</sup>.
</strong></p>

<p>For m=2s+1, the exponent &minus;k<sup>2</sup> is replaced by
&minus;k(k&minus;1), producing two equal central modes. These are discrete
theta laws and imply R<sub>m</sub>=m/2+O<sub>Pr</sub>(1). They apply only to
this explicitly defined family, not to a uniformly random subgroup of
S<sub>n</sub>.</p>

<p><strong>Verification and hostile audit.</strong> Exact-integer programs
check the formula through small vector spaces and construct the actual
permutation groups in selected cases through S<sub>9</sub>. A separate hostile
audit rebuilt the bijection without the author code, enumerated the complete
156-subgroup lattice of S<sub>5</sub>, checked 2,730 groups in the S<sub>8</sub>
p=2 slice and 4,200 groups in the S<sub>9</sub> p=3 slice, and independently
derived every sign in the asymptotics and both parity laws.</p>

<p><strong>Scope.</strong> This does not determine the unknown total for
S<sub>19</sub>, improve the global leading exponent, provide a matching global
second-order upper bound, or settle the order law for a uniformly random
subgroup. The live page had no claimed proof or current worker, and a dated
literature search did not find this order-refined formula; that is a scoped
search report, not a claim that unindexed prior work cannot exist.</p>
`,
    links: [
      { label: "erdosproblems.com/1162", url: "https://www.erdosproblems.com/1162" },
      { label: "Roney-Dougal and Tracey (2025)", url: "https://arxiv.org/abs/2503.05416" },
      { label: "OEIS A005432", url: "https://oeis.org/A005432" },
      { label: "Proof, exact checks, and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1162/order-refined-p-orbit-slice" },
    ],
  },
  {
    slug: "86-hypercube-q9-1506",
    problemNum: 86,
    title: "#86: a 1,506-edge C4-free subgraph of Q9",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "An explicit subgraph of the 9-dimensional cube has 1,506 edges and " +
      "no 4-cycle, proving ex(Q9,C4)>=1,506. Exhaustive face and " +
      "common-neighbour checks certify the graph, which improves the " +
      "identified public 1,505-edge certificate by one. This is a finite " +
      "lower bound, not an exact value or asymptotic result.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/86">erdosproblems.com/86</a>,
OPEN). The n-dimensional hypercube Q<sub>n</sub> has the binary strings of
length n as vertices, with edges between strings differing in one coordinate.
If f(n) is the largest number of edges in a C<sub>4</sub>-free subgraph of
Q<sub>n</sub>, Erdős asked whether</p>

<p style="text-align:center"><strong>
f(n)&le;(1/2+o(1))n&middot;2<sup>n&minus;1</sup>.
</strong></p>

<p>We do not resolve that asymptotic question. We improve one explicit finite
lower bound:</p>

<p style="text-align:center;font-size:1.2em"><strong>
f(9)&ge;1,506.
</strong></p>

<p><strong>The certificate.</strong> The public graph lists 1,506 distinct
pairs of vertices in {0,...,511}. Every pair differs in exactly one bit, so
every row is an edge of Q<sub>9</sub>. A four-cycle in a hypercube must
alternate two coordinate directions and is therefore one of its square
2-faces. Q<sub>9</sub> has</p>

<p style="text-align:center"><strong>
C(9,2)&middot;2<sup>7</sup>=4,608
</strong></p>

<p>such faces. Exhaustive verification finds zero faces containing all four
boundary edges. A second checker builds adjacency from scratch and examines
all 7,426 length-two paths: no unordered endpoint pair has two distinct common
neighbours. Either check proves that the graph has no C<sub>4</sub>.</p>

<p><strong>One edge beyond the identified public frontier.</strong> A May 2026
forum post supplied a 1,505-edge Q<sub>9</sub> certificate. The fixed current
repository version and graph hash are frozen in the verification package. The
new graph shares 1,313 edges with it, adds 193, and removes 192, for a net gain
of one. The public 1,505-edge graph also passes the independent checker.</p>

<p><strong>Generation and hostile audit.</strong> A deterministic min-conflicts
search starting from the public graph found the certificate; the heuristic is
provenance, not proof. Its one-thread seed-1 rerun reproduces the canonical
JSON byte for byte. The hostile audit used a strict clean-room parser,
enumerated every face and common-neighbour pair independently, and confirmed
that a controlled mutation completing one square is rejected. A decorrelated
12-thread rerun found a different valid 1,506-edge graph as well.</p>

<p><strong>Scope.</strong> This proves only f(9)&ge;1,506. It does not establish
f(9) exactly, prove optimality, or move the asymptotic bounds. The live problem
page had no claimed proof or current worker, and the current paper, forum,
OEIS, repository, and exact-code searches exposed no 1,506-edge construction
on 2026-08-11. That supports comparison with the identified public 1,505-edge
certificate, but cannot rule out private or unindexed prior work.</p>
`,
    links: [
      { label: "erdosproblems.com/86", url: "https://www.erdosproblems.com/86" },
      { label: "Public Q9=1505 certificate", url: "https://github.com/rafalwronapl/erdos86-hypercube-c4" },
      { label: "Minamoto's 2026 Q6-Q8 constructions", url: "https://arxiv.org/abs/2603.29127" },
      { label: "OEIS A245762", url: "https://oeis.org/A245762" },
      { label: "Q9=1506 graph, generator, checks, and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/86/q9-1506" },
    ],
  },
  {
    slug: "222-sums-two-squares-gap-112",
    problemNum: 222,
    title: "#222: next record gap between sums of two squares is 112",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "An exhaustive scan from zero finds the next record gap between sums " +
      "of two squares at 133,858,454,292..133,858,454,404. Its difference " +
      "is 112, so 111 consecutive interior integers are nonrepresentable. " +
      "Independent scans and a direct factor certificate prove it is the " +
      "first new record and remains maximal through 200 billion; the " +
      "asymptotic problem remains open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/222">erdosproblems.com/222</a>,
OPEN). Write n<sub>1</sub>&lt;n<sub>2</sub>&lt;&middot;&middot;&middot; for the
integers representable as sums of two squares. Problem 222 asks for good upper
and lower bounds on the consecutive differences
n<sub>k+1</sub>&minus;n<sub>k</sub>. We do not improve those asymptotic bounds,
but we extend the exact record-gap frontier.</p>

<p><strong>The new record.</strong> The consecutive represented integers</p>

<p style="text-align:center;font-size:1.15em"><strong>
133,858,454,292 &nbsp; and &nbsp; 133,858,454,404
</strong></p>

<p>differ by 112. Therefore the 111 integers strictly between them are all
nonrepresentable. This is the first record after the published difference-107
gap at 99,951,600,293..99,951,600,400, and difference 112 remains the global
maximum through the represented endpoint 200,000,000,000. The only other gap
of difference at least 108 before that endpoint is a later difference-108 gap
at 190,766,104,961..190,766,105,069.</p>

<p><strong>A direct certificate for all 111 misses.</strong> The endpoints have
the explicit representations</p>

<pre><code>133858454292 = 49986^2 + 362436^2
133858454404 = 35298^2 + 364160^2.</code></pre>

<p>For every interior integer, the public certificate supplies a prime
p&equiv;3 (mod 4) occurring to an odd exact exponent. Such an integer cannot be
a sum of two squares. Dependency-free 64-bit primality and valuation code and
PARI/GP independently verify every row, so this particular gap does not depend
on trusting the large scan.</p>

<p><strong>Why it is a record.</strong> The primary scanner enumerates every
pair 0&le;a&le;b with a<sup>2</sup>+b<sup>2</sup> in each closed chunk and marks
the resulting integers in a packed bitmap. A complete baseline from zero
recovers the published unique difference-107 maximum. Two post-anchor runs
with different chunk boundaries agree on 15,137,795,993 represented integers,
the new maximum, and the full list of gaps at least 108. A separately written
scanner reverses the coordinate loops, uses a byte array, static scheduling,
and a third partition; it produces exactly the same count and gaps.</p>

<p><strong>Hostile audit.</strong> The auditor ran a new single scan of the
entire interval 0..200,000,000,000 with a fourth chunk width. It counted
30,700,929,089 represented integers and recovered the same two large gaps.
That total also equals the two author counts after subtracting their two
represented overlap endpoints. Both scanners were separately checked against
the prime-factor characterization on 35 represented-boundary cases and random
partitions, and PARI regenerated the 111-row obstruction byte for byte.</p>

<p><strong>Scope.</strong> This is a bounded exact computational result. It
makes no assertion about the next record beyond 200 billion and does not move
the asymptotic lower or upper bounds in Problem 222. The live page had no
claimed proof or current worker, the relevant OEIS record tables still ended
at the old gap, and exact-endpoint searches found no indexed prior occurrence
on 2026-08-11. That is a dated search result, not an absolute priority claim.</p>
`,
    links: [
      { label: "erdosproblems.com/222", url: "https://www.erdosproblems.com/222" },
      { label: "OEIS A297350 — starts of record gaps", url: "https://oeis.org/A297350" },
      { label: "OEIS A357018 — record nonrepresentable runs", url: "https://oeis.org/A357018" },
      { label: "Erdős's 1951 paper", url: "https://doi.org/10.5486/PMD.1951.2.2.04" },
      { label: "Computation, obstruction certificate, and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/222/record-gap-112" },
    ],
  },
  {
    slug: "1160-group-count-m11",
    problemNum: 1160,
    title: "#1160: stronger group-count inequality holds at m = 11",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "An exact reconstruction gives 49,910,538,480 groups across all " +
      "orders below 2,048. A published exact subclass count of " +
      "1,774,274,116,992,170 at order 2,048 already exceeds that total, " +
      "certifying the stronger conjecture at m=11. The general problem " +
      "remains open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/1160">erdosproblems.com/1160</a>,
OPEN). Let g(n) be the number of isomorphism classes of groups of order n.
The original conjecture says that n&le;2<sup>m</sup> implies
g(n)&le;g(2<sup>m</sup>). A stronger question asks whether</p>

<p style="text-align:center"><strong>
&sum;<sub>n&lt;2<sup>m</sup></sub> g(n)&le;g(2<sup>m</sup>)
</strong></p>

<p>for every sufficiently large m, perhaps already for m&ge;7. We certify
this stronger inequality at m=11.</p>

<p><strong>The result.</strong> The exact group counts below 2,048 sum to</p>

<p style="text-align:center;font-size:1.2em"><strong>
&sum;<sub>n&lt;2,048</sub> g(n)=49,910,538,480.
</strong></p>

<p>Eick's 2024 survey gives an exact count of
1,774,274,116,992,170 groups of order 2,048 whose lower 2-central series has
length two. This is only a subclass of all groups of that order. Therefore</p>

<p style="text-align:center;font-size:1.15em"><strong>
49,910,538,480<br>
&lt;1,774,274,116,992,170&le;g(2,048),
</strong></p>

<p>with a certified margin of 1,774,224,206,453,690. The stronger conjecture
holds at m=11, and consequently g(n)&le;g(2,048) for every
1&le;n&le;2,048.</p>

<p><strong>Reconstructing the left side.</strong> Conway, Dietrich, and
O'Brien counted 423,171,191 groups at all positive orders below 2,048 other
than 1,024. Burrell later corrected the remaining value to</p>

<p style="text-align:center"><strong>
g(1,024)=49,487,367,289.
</strong></p>

<p>The verification bundle also reconstructs the total directly. GAP and
SmallGrp regenerate 2,034 of the 2,047 positive-order counts; the final 13
come from the published appendix. Every value agrees with the current OEIS
A000001 table, and both routes give the displayed total exactly.</p>

<p><strong>Independent audit.</strong> A hostile audit used a newer GAP and
SmallGrp release, independently parsed every appendix cell, isolated the
single stale order-1,024 entry, and checked the source statements behind both
sides of the inequality. It also found a one-unit marginal-total typo in an
unused dissertation table; the theorem value, explicit correction, GAP
count, and later survey all agree.</p>

<p><strong>Scope.</strong> This is a proof-level finite case, not a solution
of the open problem. It does not determine g(2,048), establish the statement
for m&ge;12, or prove either conjecture eventually. The live problem page had
no claimed proof or current worker on 2026-08-11, and targeted searches did
not locate this m=11 comparison; that is a dated search result, not an
absolute priority claim.</p>
`,
    links: [
      { label: "erdosproblems.com/1160", url: "https://www.erdosproblems.com/1160" },
      { label: "OEIS A000001", url: "https://oeis.org/A000001" },
      { label: "Conway-Dietrich-O'Brien count", url: "https://www.math.auckland.ac.nz/~obrien/research/gnu.pdf" },
      { label: "Burrell's correction", url: "https://doi.org/10.1080/00927872.2021.2006680" },
      { label: "Eick's 2024 survey", url: "https://doi.org/10.1007/s10208-024-09688-1" },
      { label: "Computation and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1160/m11" },
    ],
  },
  {
    slug: "168-smooth-prefix-frontier",
    problemNum: 168,
    title: "#168: computational frontier reaches f(5,020) = 3,347",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "A reproducible floating-MIP computation extends the finite-value table " +
      "for corner-free subsets of the first 3-smooth numbers from prefix " +
      "5,000 through 5,020, adding twelve OEIS A004059 rows. Two SCIP " +
      "formulations agree; no proof-carrying certificate was obtained, and " +
      "the density and irrationality questions remain open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/168">erdosproblems.com/168</a>,
OPEN). Let F(N) be the largest subset of {1,...,N} containing no triple
{n,2n,3n}. Graham, Witsenhausen, and Spencer proved that F(N)/N has a limit.
Problem 168 asks for its value and whether it is irrational. We do not resolve
either question.</p>

<p><strong>The finite reduction.</strong> Order the positive 3-smooth numbers
d<sub>1</sub>&lt;d<sub>2</sub>&lt;&middot;&middot;&middot;, where
d<sub>i</sub>=2<sup>a</sup>3<sup>b</sup>, and let f(k) be the largest subset
of the first k of them containing no corner</p>

<p style="text-align:center"><strong>
(a,b), (a+1,b), (a,b+1).
</strong></p>

<p>The original density is recovered from the increments of f. The published
OEIS A004059 table ended at f(5,000)=3,335. This computation extends the full
prefix through</p>

<p style="text-align:center;font-size:1.2em"><strong>
f(5,020)=3,347.
</strong></p>

<p>The twelve new first-hit rows are</p>

<blockquote>
f(5,002)=3,336, f(5,003)=3,337, f(5,005)=3,338,
f(5,007)=3,339, f(5,008)=3,340, f(5,010)=3,341,<br>
f(5,012)=3,342, f(5,014)=3,343, f(5,015)=3,344,
f(5,017)=3,345, f(5,018)=3,346, f(5,019)=3,347.
</blockquote>

<p><strong>How it was computed.</strong> A corner-free set is an independent
set in a 3-uniform hypergraph, equivalently the complement of a vertex cover.
SCIP solved the baseline and each of the eight new flat steps to equal reported
primal and dual bounds. At every intervening step, an explicit checked witness
gains one point; the elementary inequality f(k)&le;f(k&minus;1)+1 then proves
the next value relative to the preceding solver anchor. All 21 witnesses pass
102,585 direct corner checks.</p>

<p><strong>Independent audit.</strong> The hostile audit reconstructed the
3-smooth prefix and forbidden triples by different code. It then used selected
variables instead of complement variables, reversed variable and constraint
order, and changed SCIP's randomization. All nine anchor objectives agreed.
The audit also reproduced every witness, propagation step, source hash, and
density calculation.</p>

<p><strong>Evidence grade.</strong> Both successful upper-bound runs use
floating-point SCIP. The installed solver has no exact-arithmetic mode, and
attempts to close the same claims with CBC, Kissat, and CaDiCaL all ended
UNKNOWN. There is no DRAT/LRAT, proof-assistant theorem, or exact rational
branch-and-bound certificate. This is a well-reproduced conventional MIP
result, not proof-carrying exact mathematics.</p>

<p><strong>Density note.</strong> Extending the prefix narrows the rigorous
rational tail calculation conditional on the published historical table and
the solver anchors, but leaves the same 35 displayed digits:</p>

<p style="text-align:center"><strong>
0.80096575500655898909042032638808241...
</strong></p>

<p>The audit also found that the published A386439 program removes one tail
term before stopping. The omitted term is below 1.03&times;10<sup>&minus;38</sup>,
so it does not change those 35 digits. The original constant, its possible
irrationality, and every asymptotic question remain open.</p>
`,
    links: [
      { label: "erdosproblems.com/168", url: "https://www.erdosproblems.com/168" },
      { label: "OEIS A004059", url: "https://oeis.org/A004059" },
      { label: "Veselinov's 2026 structural paper", url: "https://arxiv.org/abs/2604.15515" },
      { label: "Computation, witnesses, and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/168/frontier-5020" },
    ],
  },
  {
    slug: "1106-partition-prime-frontier",
    problemNum: 1106,
    title: "#1106: F(n) > n certified through 10,100",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "Complete factorization gives F(115)=115 and F(116)=117. From there, " +
      "one fresh proven-prime divisor of each partition number p(n) certifies " +
      "F(n)>=n+1 for every 116<=n<=10,100. The 100 new steps extend the " +
      "published finite frontier; the eventual inequality remains open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/1106">erdosproblems.com/1106</a>,
OPEN). Let p(n) be the partition function and let F(n) count the distinct
prime divisors of</p>

<p style="text-align:center"><strong>
p(1)p(2)&middot;&middot;&middot;p(n).
</strong></p>

<p>The first question on the page, whether F(n) tends to infinity, is known:
Schinzel and Wirsing proved the stronger bound F(n)&gg;log n. The remaining
question asks whether F(n)&gt;n for all sufficiently large n. We do not settle
that asymptotic question, but we extend its verified finite range.</p>

<p><strong>The result.</strong> Exact factorization through n=116 gives</p>

<p style="text-align:center;font-size:1.2em"><strong>
F(115)=115, &nbsp; F(116)=117,
</strong></p>

<p>and a contiguous prime-divisor certificate proves</p>

<p style="text-align:center;font-size:1.2em"><strong>
F(n)&ge;n+1 for every 116&le;n&le;10,100.
</strong></p>

<p><strong>Why the certificate works.</strong> By stage 116 there are exactly
117 distinct prime factors. For each successive n from 117 through 10,100,
the certificate supplies a prime q<sub>n</sub> dividing p(n) that is absent
from the base set and different from every earlier q<sub>j</sub>. At stage n
these exhibit 117+(n&minus;116)=n+1 distinct prime divisors of the cumulative
product. This proves the inequality at every intermediate index, not just at
the endpoint.</p>

<p>The verifier recomputes p(0),...,p(10,100) exactly using Euler's
generalized-pentagonal recurrence. It completely factors the base window by
trial division, checks every one of the 9,984 witness divisions over the
integers, checks freshness, and asks PARI/GP's rigorous <code>isprime</code>
routine to prove every witness prime. The final exhibited set has 10,101
distinct primes.</p>

<p><strong>Independent audit.</strong> A hostile audit reran the whole chain
with PARI/GP's built-in <code>numbpart</code>, rather than the author's
recurrence. It also rebuilt the base partition numbers by coefficient dynamic
programming and refactored them with a separate engine. Both routes reproduce
the exact 115- and 117-prime base counts, all 9,984 divisibility and primality
checks, and the running lower bound through 10,100.</p>

<p><strong>Scope.</strong> OEIS A194259 and A194261 published data through
10,000 on the access date. The genuinely new part of this certificate is the
100-index continuation from 10,001 through 10,100, relative to those dated
records and the searches preserved in the bundle. We do not compute exact
values of F(n) after 116, claim absolute literature priority, or prove that
F(n)&gt;n eventually.</p>
`,
    links: [
      { label: "erdosproblems.com/1106", url: "https://www.erdosproblems.com/1106" },
      { label: "OEIS A194259", url: "https://oeis.org/A194259" },
      { label: "OEIS A194261", url: "https://oeis.org/A194261" },
      { label: "Certificate and hostile audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1106/frontier-10100" },
    ],
  },
  {
    slug: "773-square-sidon-frontier",
    problemNum: 773,
    title: "#773: conditional exact values a(69) = 32 and a(70) = 33",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "Problem #773 asks whether the largest Sidon subset of the first N " +
      "positive squares has size N^(1-o(1)); that asymptotic problem remains " +
      "open. Conditional on the full published exact OEIS A390813 prefix " +
      "through N=68, a frozen exhaustive search proves the next two values: " +
      "a(69)=32 and a(70)=33. The upper search at 69 covers seven disjoint " +
      "cubes and 171,546,643 recursive states; the size-32 and size-33 lower " +
      "witnesses are direct integer certificates. Two hostile audits reran " +
      "the proof and checked its reduction independently. This extends a " +
      "finite table, not the exponent in Erdős's question.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/773">erdosproblems.com/773</a>,
OPEN). Let a(N) be the largest size of a Sidon subset of
{1<sup>2</sup>,...,N<sup>2</sup>}: every unordered sum i<sup>2</sup>+j<sup>2</sup>,
including the diagonal i=j, must be different. Erdős asked whether</p>

<p style="text-align:center"><strong>a(N)=N<sup>1-o(1)</sup>.</strong></p>

<p>We do not settle that asymptotic question. We extend its exact finite
frontier by two places.</p>

<p><strong>The result.</strong> Conditional on the full published exact
<a href="https://oeis.org/A390813">OEIS A390813</a> prefix through N=68,</p>

<p style="text-align:center;font-size:1.2em"><strong>
a(69)=32 and a(70)=33.
</strong></p>

<p>The condition is substantive and explicit. The frozen proof uses the
published upper bounds a(k) for every remaining prefix 1,...,k with k&le;68;
it does not independently re-prove those earlier values. The final published
value a(68)=32 first forces any hypothetical 33-set at N=69 to contain
69<sup>2</sup>. The computation then fixes index 69 and asks whether 32 more
indices can be chosen from 1,...,68.</p>

<p><strong>An exact finite model.</strong> A collision is an equality</p>

<p style="text-align:center"><strong>
i<sup>2</sup>+j<sup>2</sup>=k<sup>2</sup>+l<sup>2</sup>
</strong></p>

<p>between different unordered pairs. After fixing 69, the checker reconstructs
all 712 minimal forbidden supports: 21 triples and 691 quadruples. A selected
index set is square-Sidon exactly when it contains none of them. There is no
floating-point arithmetic in this reduction or in the search.</p>

<p><strong>The exhaustive upper search.</strong> At each node, three independently
audited rules bound the remaining extension: the frozen published prefix value
a(k), vertices forced out by an almost-complete forbidden support, and a clique
partition of the live pair-conflict graph. The last rule is valid because a
Sidon extension can take at most one vertex from each conflict clique.</p>

<p>The assignments to (x<sub>68</sub>,x<sub>67</sub>,x<sub>66</sub>) split into
the following seven disjoint cubes:</p>

<blockquote>00, 010, 011, 100, 101, 110, 111.</blockquote>

<p>The first cube includes both possible values of x<sub>66</sub>, so the list is
also exhaustive. Every cube returned UNSATISFIABLE. In total the proof search
visited 171,546,643 recursive states and made 167,258,147 conflict-coloring
calls. Therefore no 33-set exists at 69, relative to the frozen OEIS prefix.</p>

<p><strong>The lower certificates.</strong> The following 32 indices give 528
pairwise distinct unordered square sums at N=69:</p>

<blockquote>3, 4, 6, 12, 13, 15, 17, 19, 23, 25, 28, 34, 35, 38, 42,
45, 48, 49, 53, 54, 56, 57, 58, 60, 61, 62, 63, 64, 65, 66, 68, 69.</blockquote>

<p>At N=70, these 33 indices give 561 distinct sums:</p>

<blockquote>1, 4, 6, 7, 9, 10, 12, 13, 16, 18, 19, 22, 24, 28, 30,
34, 36, 37, 39, 40, 43, 46, 49, 51, 52, 57, 58, 60, 64, 65, 67, 69, 70.</blockquote>

<p>Both are unconditional integer certificates. Deleting index 70 from any
candidate shows a(70)&le;a(69)+1, so the second witness gives equality once
the conditional value at 69 is established.</p>

<p><strong>Audit posture.</strong> The bundle freezes the exact OEIS b-file and
its hash, the proof source, all seven completed logs, witnesses, and independent
checkers. The primary audit rebuilds the optimized executable byte-for-byte and
reconstructs the supports, cube cover, logs, and witnesses. One hostile audit
then reran all seven cubes from source, reproduced every counter exactly, and
passed a sanitizer plus incremental-state check on a deep subcube. A second
independent hostile audit reviewed the proof and artifact package separately
before publication.</p>

<p><strong>Scope.</strong> This is a rigorous computational extension conditional
on the existing exact table, not a claim that the OEIS prefix has been
re-certified here and not progress on the exponent in Erdős's question. The
site also records a July CODEX attempt on #773 that found no proof; this is a
new finite round, not our first encounter with the problem.</p>
`,
    links: [
      { label: "erdosproblems.com/773", url: "https://www.erdosproblems.com/773" },
      { label: "OEIS A390813", url: "https://oeis.org/A390813" },
      { label: "Proof search, witnesses, logs, and hostile audits", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/773/n69-frontier" },
    ],
  },
  {
    slug: "617-ramsey-edge-frontier",
    problemNum: 617,
    title: "#617: the exact edge floor for every candidate color class",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "Problem #617 asks whether every r-coloring of K_(r^2+1) has an " +
      "(r+1)-vertex clique missing a color. That remains open beyond the known " +
      "cases r=3,4. We prove an exact auxiliary theorem for every r>=2: the " +
      "fewest edges in an (r^2+1)-vertex graph with neither a clique nor an " +
      "independent set of size r+1 is (r^3-r^2+4r-2)/2. Thus every color " +
      "class in a hypothetical counterexample has at least 59 edges at r=5. " +
      "The five bounds total 295 of 325 edges, leaving a real 30-edge " +
      "compatibility gap, so this is a structural frontier rather than a solve.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/617">erdosproblems.com/617</a>,
FALSIFIABLE). Erdős and Gyárfás conjectured that every coloring of the edges of
K<sub>r<sup>2</sup>+1</sub> with r colors has r+1 vertices whose induced clique
misses at least one color. They proved this for r=3 and r=4. We do not prove the
next case r=5.</p>

<p><strong>The color-class reduction.</strong> Suppose instead that a balanced
coloring exists, meaning every (r+1)-vertex clique contains every color. Fix one
color and let G be the graph formed by its edges. An independent set of size
r+1 would miss that color. A clique of size r+1 would use only that color and
miss all the others. Therefore every color graph must satisfy</p>

<p style="text-align:center"><strong>
&alpha;(G)&le;r and &omega;(G)&le;r.
</strong></p>

<p>We determined the exact cheapest possible graph with those two properties.
For every integer r&ge;2, define</p>

<p style="text-align:center"><strong>
m<sub>r</sub>=min{e(G): |V(G)|=r<sup>2</sup>+1,
&alpha;(G),&omega;(G)&le;r}.
</strong></p>

<p>Then</p>

<p style="text-align:center;font-size:1.2em"><strong>
m<sub>r</sub>=(r<sup>3</sup>&minus;r<sup>2</sup>+4r&minus;2)/2.
</strong></p>

<p><strong>The lower bound.</strong> Put H equal to the complement of G.
The bound &alpha;(G)&le;r says H is K<sub>r+1</sub>-free. Meanwhile
&alpha;(H)=&omega;(G)&le;r, so coloring the r<sup>2</sup>+1 vertices of H
requires at least r+1 colors; H is not r-partite.</p>

<p>Kang and Pikhurko's exact stability theorem determines the largest edge
count of precisely such a graph. At n=r<sup>2</sup>+1 their Theorem 1 gives</p>

<p style="text-align:center"><strong>
e(H)&le;t<sub>r</sub>(n)&minus;&lfloor;n/r&rfloor;+1
=t<sub>r</sub>(n)&minus;r+1,
</strong></p>

<p>where t<sub>r</sub>(n) is the balanced Turán number. Its part sizes are
r+1,r,...,r. Complementing and simplifying gives
e(G)&ge;(r<sup>3</sup>&minus;r<sup>2</sup>+4r&minus;2)/2.</p>

<p><strong>A construction attaining it.</strong> Start with K<sub>r,r+1</sub>
on parts X and Y. Choose y<sub>1</sub>,y<sub>2</sub> in Y, add the edge
y<sub>1</sub>y<sub>2</sub>, and for every x in X delete exactly one of
xy<sub>1</sub>,xy<sub>2</sub>, using both deletion choices. Call the resulting
graph J. It has r<sup>2</sup>+1 edges, is triangle-free, and has
&alpha;(J)=r.</p>

<p>Now take the disjoint union of r&minus;2 copies of K<sub>r</sub> and the
complement of J. This graph has r<sup>2</sup>+1 vertices, exactly the displayed
number of edges, and both clique and independence number r. For r=2 the clique
part is empty and the construction is simply C<sub>5</sub>.</p>

<p><strong>What this says at r=5.</strong> Every one of the five color classes
in a counterexample on K<sub>26</sub> would need at least</p>

<p style="text-align:center;font-size:1.2em"><strong>m<sub>5</sub>=59 edges.</strong></p>

<p>The lower bounds consume 5&middot;59=295 of the 325 edges. More generally the
unallocated slack is exactly r(r&minus;1)(r&minus;2)/2; at r=5 it is 30.
That gap matters: this theorem constrains each color separately but does not
show whether five such graphs can partition K<sub>26</sub>.</p>

<p><strong>Audit posture.</strong> The lower proof depends only on the published
Kang&ndash;Pikhurko theorem, whose exact hypotheses and both parameter branches
were checked against the official paper. The upper construction is elementary.
At r=5, two independent standard-library checkers start from different graph
representations and verify 59 edges, clique number 5, and independence number
5; one directly exhausts all 230,230 six-vertex subsets. A third checker tests
the general construction and polynomial identities, while the written case
proof supplies the universal quantifier. An ultra cold audit reproduced the
bundle and caught the r=2 wording boundary before publication.</p>

<p><strong>Scope.</strong> This is a derived auxiliary consequence, not a claim
of literature priority for a resolution of #617. The site also had a May 2026
ledger attempt concerning affine K<sub>25</sub> extensions; this is a separate
second round. The simultaneous color-partition problem, including r=5, remains
open.</p>
`,
    links: [
      { label: "erdosproblems.com/617", url: "https://www.erdosproblems.com/617" },
      { label: "Proof, checkers, source snapshot, and cold audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/617/edge-frontier" },
      { label: "Kang-Pikhurko (2005), official article page", url: "https://matstud.org.ua/texts/2005/24_1/24_1_012_020.html" },
    ],
  },
  {
    slug: "295-k17-exact",
    problemNum: 295,
    title: "#295: k(17) = 32, and now 33 ≤ k(18) ≤ 35 by exact exhaustion",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "Problem #295 asks whether the shortest unit-fraction expansion above a " +
      "denominator cutoff eventually exceeds (e−1)N by an unbounded amount. " +
      "That asymptotic problem remains open. Round 1 closed k(17)=32. Round 2 " +
      "now proves the rigorous computational bounds 33≤k(18)≤35. The harmonic " +
      "maximum excludes at most 30 terms; exact GMP and Fraction recursions " +
      "independently execute the same proved exhaustive search and exclude 31 " +
      "and 32. A transparent four-for-one unit-fraction surgery on the k(17) " +
      "identity supplies 35 terms beginning at 18. Full reproduction, sanitizer, " +
      "serial, concurrency, and hostile source audits passed. Whether k(18) is " +
      "33, 34, or 35 remains open, as does Erdős's asymptotic question.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/295">erdosproblems.com/295</a>,
OPEN). Let k(N) be the fewest distinct increasing denominators
N≤n<sub>1</sub>&lt;⋯&lt;n<sub>k</sub> whose reciprocals sum to 1. Erdős asked whether</p>

<p style="text-align:center"><strong>k(N)−(e−1)N → ∞.</strong></p>

<p>We did not solve that asymptotic question.</p>

<p><strong>Round 2 (11 August): the next cutoff is narrowed to three values.</strong>
The new exact computational result is</p>

<p style="text-align:center;font-size:1.2em"><strong>
33 ≤ k(18) ≤ 35.</strong></p>

<p><strong>The elementary part of the lower bound.</strong> Among any t distinct
denominators at least 18, the largest reciprocal sum comes from the consecutive
integers 18,…,17+t. For t=30 that sum is exactly</p>

<p style="text-align:center"><strong>
442017301628992345493 / 442720643463713815200 &lt; 1.
</strong></p>

<p>Thus 30 or fewer terms are impossible. At 31 terms the harmonic maximum
crosses 1, so the next two lengths require a genuine exhaustive search.</p>

<p><strong>The exact exclusions at 31 and 32.</strong> The same finite recurrence
proved below was implemented twice: once with GMP integers and rationals and a
static threaded frontier, and once with Python arbitrary-size integers and
<code>fractions.Fraction</code> using a different multiprocessing split and
terminal implementation. Both completed with no expansion and exactly the
same counters:</p>

<ul>
<li>31 terms: 20,293 states, 13,139 two-term states, and 69,727 scanned first denominators;</li>
<li>32 terms: 14,678,224 states, 11,753,049 two-term states, and 114,603,091 scanned first denominators.</li>
</ul>

<p>The terminal formula forces the last denominator algebraically and never
caps it. Both engines were separately tested on a completion whose forced last
denominator is 10<sup>100</sup>. Every branch deletion is an exact rational
comparison; floating point can only retain extra work. The optional
factorization path was never reached in either proof run.</p>

<p><strong>The 35-term upper certificate.</strong> Starting from the Round-1
identity, replace 1/17 by</p>

<p style="text-align:center"><strong>
1/31 + 1/40 + 1/640 + 1/337280 = 1/17.
</strong></p>

<p>This gives the following 35 strictly increasing denominators, all at least
18, whose reciprocals sum exactly to 1:</p>

<blockquote>18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
32, 33, 34, 35, 36, 38, 39, 40, 42, 43, 44, 45, 48, 50, 52, 54, 63,
640, 337,280, 1,735,650, 68,479,214,496.</blockquote>

<p>The replacement is itself an integer certificate:
(10880+8432+527+1)/337280=19840/337280=1/17. Exact Fraction arithmetic
checks the complete source identity, the surgery, strict ordering, and the
new complete sum.</p>

<p><strong>Audit posture.</strong> A hostile audit rebuilt and reproduced the
whole package, reran the full 32-term search under AddressSanitizer and
UndefinedBehaviorSanitizer, checked the threaded search under ThreadSanitizer,
and reran the Fraction engine serially with multiprocessing removed. It found
no load-bearing gap. The two engines share the same proved recurrence lineage,
so their agreement is an arithmetic and implementation cross-check, not a
second mathematical method. Accordingly, k(18)≥33 is labelled a rigorous
computational result, not an elementary proof.</p>

<p><strong>What remains at 18.</strong> We have not found a 33- or 34-term
identity, nor excluded either length; k(18) could be 33, 34, or 35. None of
these finite computations settles the original asymptotic question.</p>

<p><strong>Round 1: the first missing finite value.</strong> We closed the first undecided
finite value beyond the existing tables:</p>

<p style="text-align:center;font-size:1.2em"><strong>k(17)=32.</strong></p>

<p><strong>The upper certificate.</strong> The following 32 distinct denominators
are increasing, begin at 17, and have reciprocal sum exactly 1:</p>

<blockquote>17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
32, 33, 34, 35, 36, 38, 39, 42, 43, 44, 45, 48, 50, 52,
54, 63, 1,735,650, 68,479,214,496.</blockquote>

<p>Their least common multiple is L=200,301,702,400,800, and direct integer
addition gives ΣL/d=L. Thus k(17)≤32 with no numerical approximation.</p>

<p><strong>Why the lower search is finite.</strong> At a state with positive
reduced remainder R=a/b, t terms left, and next denominator at least D, every
possible first denominator d lies in the exact interval</p>

<p style="text-align:center"><strong>
max(D,⌊b/a⌋+1) ≤ d ≤ ⌊tb/a⌋.</strong></p>

<p>The left inequality leaves room for a positive tail; the right follows from
R≤t/d. After choosing d, the largest possible sum of the remaining distinct
fractions is 1/(d+1)+⋯+1/(d+t−1). If that is smaller than R−1/d, the branch is
impossible. Moreover 1/d plus this maximal tail decreases strictly with d, so
the first failure discards every later child. These are exact rational tests.</p>

<p><strong>The unbounded final denominator is not truncated.</strong> For the last
two terms, an ordered solution D≤x&lt;y of a/b=1/x+1/y is equivalent to</p>

<p style="text-align:center"><strong>(ax−b)(ay−b)=b².</strong></p>

<p>Writing q=ax−b, the program either scans every admissible x or enumerates every
divisor q of b² with q&lt;b, q≡−b (mod a), and q≥aD−b. Then
x=(b+q)/a and y=(b+b²/q)/a. This covers arbitrarily large y; there is no hidden
denominator cap.</p>

<p><strong>The exact exclusion.</strong> The 28 largest possible terms already sum
to 9,344,202,253,751,673,739 / 9,419,588,158,802,421,600, which is below 1.
The exhaustive runs then returned:</p>

<ul>
<li>29 terms: 1,667 states, none;</li>
<li>30 terms: 1,461,942 states, none;</li>
<li>31 terms: 447,526,713 states, 382,969,084 two-term states,
5,721,929,705 direct-scan candidates, none.</li>
</ul>

<p>Only two terminal ranges were wide enough for divisor enumeration. They used
b=219,060,189,739,591,200 and b=9,419,588,158,802,421,600, both factoring
completely over the displayed small primes in the verifier log. A separate
standard-library Python meet-in-the-middle enumeration checked respectively
11,366,932 and 34,100,797 divisors below b in the required residue classes and
found none.</p>

<p><strong>Audit posture.</strong> We ran the 31-term computation three times across
two C++ implementations and different thread counts; every state and candidate
total agrees exactly. The newest implementation uses a fixed 18,727-task
frontier with atomic exactly-once assignment. Floating point can only retain
extra work: every actual branch deletion is confirmed by GMP exact arithmetic.
An adversarial code review found no skipped branch, overflow on this instance,
or race. The implementation is decorrelated, not an algorithmically independent
method — its author had read the earlier depth-first searches — so the lower
bound remains an exact computational result, not an elementary proof.</p>

<p><strong>The OEIS connection.</strong> A192881 asks for the shortest expansion
whose first term is exactly 1/n and currently ends at n=16. The lower search
allows the first denominator to be any value at least 17, while our upper
identity actually starts at 17. Therefore the same result also gives
<strong>a(17)=32</strong>.</p>

<p><strong>What remains.</strong> The original problem needs a uniform arithmetic
obstruction forcing k(N)−(e−1)N to grow. Exact recursion scales exponentially
and does not provide that. The persistent structural clue is p-adic: for every
prime in the common denominator, the largest denominator valuation must occur
at least twice. No known argument yet turns those overlapping prime-by-prime
constraints into an unbounded global excess.</p>
`,
    links: [
      { label: "erdosproblems.com/295", url: "https://www.erdosproblems.com/295" },
      { label: "Verification code, exact-search logs, and k(18) hostile-audit bundle", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/295" },
      { label: "OEIS A192881", url: "https://oeis.org/A192881" },
      { label: "Erdős–Graham, Old and New Problems and Results in Combinatorial Number Theory (1980), p. 35", url: "https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf" },
      { label: "Ruderman–Erdős–Straus, solution of E2232 (1971)", url: "https://doi.org/10.2307/2317539" },
    ],
  },
  {
    slug: "552-c4-star-46-vertex-witness",
    problemNum: 552,
    title: "#552: the missing finite Ramsey value is 46",
    date: "2026-08-11",
    status: "partial",
    summary:
      "An unreviewed public candidate proof gives R(C₄,K₁,₃₉)=46, closing the " +
      "first bracketed entry in the finite table. Our hostile audit reconstructed " +
      "the 45-vertex lower witness, the universal 46-vertex reduction, the exact " +
      "spectral moments, and a rational dual certificate, and found the finite " +
      "proof valid without relying on the candidate's uncertified SAT logs. This " +
      "is an independently audited candidate result, not yet peer reviewed and " +
      "not a solution of the asymptotic Erdős problem.",
    links: [
      { label: "erdosproblems.com/552", url: "https://www.erdosproblems.com/552" },
      { label: "Audited candidate proof at exact Git commit", url: "https://github.com/zach7036/c4-star-ramsey/tree/86a1c5055eea5e3891b2eeaea6c7ee1b3977bd33" },
      { label: "Independent audit, exact checker, and frozen sources", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/552/r-c4-k1-39-46" },
      { label: "Radziszowski, Small Ramsey Numbers, revision #18 (24 Apr 2026) — item 3.3.2(d) and Table IVa", url: "https://www.cs.rit.edu/~spr/ElJC/ejcram18.pdf" },
      { label: "Our archived 4 August working report for #552", url: "/report/552" },
    ],
    body: `
<p><strong>Update, 11 August 2026.</strong> At public Git commit
<code>86a1c505...</code>, an unreviewed candidate proof gives</p>

<blockquote><strong>R(C₄,K<sub>1,39</sub>) = 46.</strong></blockquote>

<p>We treated the repository as adversarial rather than inheriting its conclusion. A separate
standard-library checker reconstructed the 45-vertex lower witness, checked the complete reduction
of a hypothetical 46-vertex counterexample, rederived every trace moment, and verified an exact
rational polynomial certificate. The audit passed. The candidate's 144 SAT status lines have no
checked proof artifacts and are therefore <em>not</em> used in this conclusion.</p>

<p><strong>The proof capsule.</strong> A C₄-free graph on 46 vertices with minimum degree at
least 7 would first be forced to be 7-regular. A local parity argument then forces every vertex
into exactly three edge-disjoint triangles; the seventh incident edge at each vertex forms part
of a perfect matching.
If A is the adjacency matrix and D joins pairs with no common neighbour, then D is cubic and</p>

<blockquote>A² = 6I + J − D.</blockquote>

<p>Hence every non-principal eigenvalue θ of A lies in
[-3,−√3]∪[√3,3]. Their first moments are exactly</p>

<blockquote>(s₀,s₁,s₂,s₃,s₄) = (45,−7,273,−67,1785),<br>
s₅ = T−615, &nbsp;0 ≤ T ≤ 92.</blockquote>

<p>Put</p>

<blockquote>q(x) = (2x+5)²(3x+5)(4904x²−38072x+85705) / 26468750.</blockquote>

<p>On the negative spectral interval q≤0, while on the positive interval q≤1 because
1−q(x) factors as
(3−x)(2x−5)²(14712x²+101560x+210075)/26468750. Substituting the exact moments gives,
for every admissible T,</p>

<blockquote>21 &lt; Σq(θ) ≤ N<sub>+</sub> ≤ Σ(1−q(−θ)) &lt; 22,</blockquote>

<p>where N<sub>+</sub> is the integer number of positive non-principal eigenvalues. That is
impossible, so the 46-vertex witness sought below does not exist. The audited 45-vertex graph has
minimum degree 6 and is C₄-free, giving the matching lower bound.</p>

<p><strong>Provenance and limits.</strong> The lower bound 46 was already established; the
candidate supplies the upper bound. This is not a consequence of Boza's <code>/46</code> table
cell, which has a wheel-index transcription error. The same order-40 wheel is Zhang's
W<sub>39</sub>=K₁+C<sub>39</sub> under rim-length indexing and W<sub>40</sub> under total-order
indexing. A second unreviewed public repository also claims the value using LRAT artifacts, but
its proof archive was not available for this audit. We make no priority claim. Most importantly,
the exact finite value does not settle the asymptotic question in Problem 552, which remains open.</p>

<p><strong>Archived search record, 4 August 2026.</strong> The analysis below records how we
narrowed the then-open 46-vertex case. Its final status paragraph is superseded by the exact proof
above, but the structural reductions and the failed construction routes remain useful.</p>

<p><strong>The historical target</strong> (<a href="https://www.erdosproblems.com/552">erdosproblems.com/552</a>,
OPEN). Determine the Ramsey number R(C₄,Sₙ), where Sₙ=K<sub>1,n</sub> is the star on
n+1 vertices. Write f(n)=R(C₄,K<sub>1,n</sub>). Parsons proved f(n) ≤ n+⌈√n⌉+1 in the
1970s, with equality at n=q² and n=q²+1 for prime powers q. Radziszowski's
<em>Small Ramsey Numbers</em>, revision #18 (24 April 2026), records that <em>every</em>
value f(n) is known for n ≤ 38 — and its Table IVa lists exactly one bracketed entry:
<strong>f(39) ∈ {46,47}</strong>. That is the first open value, and it is where we aimed.</p>

<p><strong>The translation, re-derived rather than inherited.</strong>
f(n) ≥ N+1 exactly when some graph on N vertices is C₄-free and its complement contains
no K<sub>1,n</sub> — i.e. every vertex has complement-degree ≤ n−1, i.e. degree ≥ N−n.
At n=39, N=46 that reads:</p>

<blockquote><strong>A witness is a C₄-free graph on 46 vertices with minimum degree ≥ 7.
It exists ⟺ R(C₄,S₃₉)=47. It doesn't ⟺ R(C₄,S₃₉)=46.</strong></blockquote>

<p>Throughout, "C₄-free" is used in the form <em>every pair of vertices has at most one
common neighbour</em>.</p>

<p><strong>1. The witness must be exactly 7-regular — and this needed a proof.</strong>
The prior write-up asserted 7-regularity. It doesn't follow from the obvious count: the
codegree bound Σ<sub>v</sub>C(d<sub>v</sub>,2) ≤ C(46,2)=1035 happily tolerates degrees up
to 13. Here is the argument that does work. In a C₄-free graph N(v) induces a matching (if
u∈N(v) had two neighbours w,x∈N(v), then w and x would share both u and v). So each
u∈N(v) sends deg(u)−1−t<sub>u</sub> edges out to distance-2 vertices, and those sets are
pairwise disjoint — a shared vertex plus v is a C₄. Hence
n ≥ 1+d+d(δ−1)−2⌊d/2⌋. With δ=7 a degree-8 vertex forces <strong>n ≥ 49 &gt; 46</strong>.
Degree 9 forces 56. So no vertex exceeds 7, and minimum degree 7 makes it regular.</p>

<p>The same count at a 7-regular vertex gives |D₂(v)| = 42−2t(v), so 46 ≥ 50−2t(v) and
<strong>every vertex lies in 2 or 3 triangles</strong>, with exactly 2t(v)−4 vertices at
distance ≥ 3.</p>

<p><strong>2. The automorphism group is a 2-group.</strong> Let σ be an automorphism of
prime order p, with orbits of size p or 1 and 46 = pm+F. For a fixed vertex f, N(f) is
σ-invariant, so 7 = pa+b with 0 ≤ b ≤ F−1. That alone kills p = 3, 5, 11, 13, 41, 43. For
p = 17, 19, 29, 31, 37 the only solution has a=0, which forces the F fixed points to carry
a 7-regular C₄-free graph among themselves — impossible, since F·C(7,2) &gt; C(F,2).</p>

<p><em>p=7</em> dies structurally, and prettily. 46 = 6·7+4, and orbit-degree forces
(a,b)=(1,0): each of the four fixed points joins exactly one full 7-orbit and no fixed
point. Two fixed points on the same orbit would share seven neighbours, so they sit on four
distinct orbits; relabel f<sub>i</sub> ~ O<sub>i</sub>. Then the within-orbit set C<sub>i</sub>
is empty (else a and a+2c share both a+c and f<sub>i</sub>), and |D<sub>ij</sub>| ≤ 1 for
every j (else d≠d′ make a and a+(d−d′) share a+d as well as f<sub>i</sub>). But the degree
equation now needs 6 from only five other orbits, each contributing at most 1. Contradiction.</p>

<p><em>p=23</em> dies by exhaustion. One 23-orbit plus 23 fixed points is impossible
because a fixed point's neighbourhood inside the orbit is invariant, hence empty or all 23.
Two 23-orbits reduce — via the abelian lemma below — to two 23-cycles with five cross
differences, and we generated and tested all <strong>80,465</strong> normalised cases.
None is C₄-free.</p>

<p><strong>3. No witness is vertex-transitive.</strong> The only groups of order 46 are
Z₄₆ and D₂₃. The circulant half is instant, via a lemma worth stating on its own: <em>no
Cayley graph on an abelian group of degree ≥ 3 is C₄-free</em> — pick s∈S; since |S| ≥ 3
and S=−S there is t∈S with t ≠ s,−s, and then 0, s, s+t, t are four distinct vertices
forming a C₄. Commutativity simply hands you the square. For the dihedral half we
generated and tested all <strong>716,496</strong> symmetric degree-7 connection sets on
D₂₃. Zero survivors.</p>

<p><strong>4. Involutions have at most 8 fixed points.</strong> If σ swaps u and u′, then
σ fixes F pointwise and σ(N(u))=N(u′), so N(u)∩F = N(u′)∩F — meaning every fixed
neighbour of u is a <em>common</em> neighbour of u and u′. C₄-freeness therefore gives
<strong>|N(u)∩F| ≤ 1</strong>. Two consequences: each pair attaches to at most one fixed
point, which forces e<sub>F</sub> ≥ 4F−23 and dies against the extremal values ex(F;C₄) at
F = 10, 12, 14; and u keeps ≥ 6 neighbours among the non-fixed vertices, so that induced
graph is C₄-free of minimum degree 6 and needs ≥ 31 vertices, giving F ≤ 14. Surviving
types: <strong>F ∈ {0,2,4,6,8}</strong>.</p>

<p><strong>5. The polarity-graph construction is dead.</strong> The Erdős–Rényi graph ER₇
is what anyone would try: 57 vertices, C₄-free, 224 edges, eight vertices of degree 7 and
forty-nine of degree 8. We need 46 vertices of minimum degree 7, so delete 11 while no
surviving degree-7 vertex loses anything and no surviving degree-8 vertex loses two.
Counting the edge endpoints leaving the deleted set D, with j of its vertices absolute,
gives e<sub>D</sub> ≥ 25−j, against ex(11;C₄)=18 — which kills every j ≤ 6 outright. For
j = 7 and 8 the absolute points form a <strong>conic</strong>, hence are pairwise
non-adjacent: two adjacent absolute points would make every point of their line absolute,
i.e. the conic a line, and no three points of a conic are collinear. The Zarankiewicz bound
on what is left then caps e<sub>D</sub> at 17 and 14, against the required 18 and 17.
Every deletion pattern fails.</p>

<p><strong>6. A spectral surprise.</strong> Let K be the 0/1 matrix of codegree-<em>zero</em>
pairs. Then identically A² = 6I+J−K, and since A²·1 = 49·1 while J·1 = 46·1, we get
K·1 = 3·1: <strong>K is a cubic graph</strong>. Prettier still, at each vertex its three
K-edges split as (7−2t(v)) graph-edges in no triangle plus (2t(v)−4) distance-3 pairs, and
those sum to 3 for <em>either</em> value of t(v). On 1<sup>⊥</sup> we have K = 6I−A², so A
and K are simultaneously diagonalisable with μ = 6−λ², and K cubic means μ ∈ [−3,3]:</p>

<blockquote><strong>every non-principal eigenvalue satisfies |λ| ∈ [√3, 3]</strong></blockquote>

<p>for a 7-regular graph, where 2√(k−1) = 2√6 ≈ 4.899. Tighter than Ramanujan. It is a
severe constraint but not a proof. It does force one thing outright: an integral spectrum
would put all 45 non-principal eigenvalues in {&plusmn;2, &plusmn;3}, and with p of them at
|&lambda;|=3 and q at |&lambda;|=2 we would need p+q=45 and 9p+4q=273, i.e. 5p=93. Not an
integer, so <strong>the witness is not an integral graph</strong> &mdash; in particular not
strongly regular. But it does not close the question: we ran the moment problem on the band
as a linear program and it is feasible, so the spectrum alone does not close the question. The moments
Σλ = −7, Σλ² = 273 and Σλ⁴ = 1785 are unconditional (the last because tr A⁴ = Σ(A²)²<sub>ij</sub>
= 46·49 + 2·966), and cross-check exactly against tr K = 0 and tr K² = 138. Σλ³ = 6T−343
depends on the triangle count T, which is 46 only if no vertex sits in just two triangles —
a step we inherited from the earlier write-up and did <em>not</em> re-verify, so we ran the
LP across the whole admissible range 31 ≤ T ≤ 46.</p>

<p><strong>What we got wrong.</strong> Worth recording, because it is the exact failure
that produces a false positive. For the fixed-point-free case we wrote down a
characterisation of the Z₂-voltage lift and it was <em>incomplete</em> — necessary but not
sufficient. An adversarial pass checked it over every quotient on 3–6 nodes against every
voltage and every internal-edge pattern (9,182,408 configurations) and found
<strong>795,512</strong> that satisfy our stated conditions and still contain a C₄. The
complete list needs three conditions: the degree-6 nodes independent in Q, every triangle
through such a node carrying voltage sum 0, and every 4-cycle of Q carrying voltage sum 1.
A nonexistence conclusion from the weak list would still have been sound; an
<em>existence</em> claim would not.</p>

<p><strong>Historical status on 4 August.</strong> At that time this was not closed. A witness,
if one existed, had to be a 7-regular
C₄-free graph on 46 vertices whose automorphism group is a 2-group in which every
involution has at most 8 fixed points; it is not vertex-transitive, admits no automorphism
of odd prime order, and does not arise by deletion from ER₇. What is left is the involution
cases F ∈ {0,2,4,6} and the trivial-automorphism case — <strong>F = 8 was eliminated on 5 Aug</strong>, when its σ-invariant instance came back UNSAT from CaDiCaL after 27.5 hours. That verdict is a solver assertion, not a checked certificate (a proof for a 27-hour UNSAT is impractical to emit); a decorrelated kissat run on the same CNF is the available cross-check. The remaining four instances were still undecided at 27+ hours each. Every script, each carrying
positive controls its checkers must pass before any verdict is trusted, is in the working
repo. The 11 August exact spectral certificate above now proves that none of these remaining
cases can exist.</p>
`,
  },
  {
    slug: "126-pairwise-sum-smooth",
    problemNum: 126,
    title: "#126: a strong partial — the conjecture reduces to one missing S-unit theorem, and the local route is provably dead",
    date: "2026-07-27",
    status: "partial",
    summary:
      "#126 asks whether f(n)/log n → ∞, where f(n) is the fewest distinct " +
      "primes that can support all pairwise sums of an n-element set — " +
      "equivalently N(s)=exp(o(s)), N(s) being the largest set whose pair " +
      "sums use ≤s primes. The window (½+o(1))s·log s ≤ N(s) ≤ 2^s has been " +
      "open since Erdős–Turán. We didn't prove it and found no " +
      "counterexample — but a strong partial: the conjecture reduces cleanly " +
      "to ONE missing theorem (a uniform subexponential bound for binary " +
      "S-unit equations over ℚ), the key extra structure is identified (the " +
      "problem needs a clique of mutually compatible S-unit solutions, not " +
      "the star a single binary equation gives), and the old local " +
      "prime-by-prime route is provably dead. N(2)=4 exactly, plus explicit " +
      "f(14)≤8 and f(21)≤12 — all verified on our side.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/126">erdosproblems.com/126</a>,
OPEN). For a finite set A of positive integers, let P(A) be the set of primes
dividing at least one pairwise sum a+b (a≠b), and f(n) the minimum of |P(A)|
over n-element A. How small can f(n) be — does f(n)/log n → ∞? Invert it:
N(s) is the largest |A| whose pair sums are all supported on some set of s
primes, so f(n)≤s ⟺ N(s)≥n, and the conjecture is exactly N(s)=exp(o(s)). The
interval construction A={1,…,⌊(p_{s+1}−1)/2⌋} (every pair sum is below the
(s+1)-st prime) gives N(s)≥(½+o(1))s·log s; Erdős–Turán proved
N(s)≤3·2^{s−1}−1, later sharpened to N(s)≤2^s in the Erdős–Surányi book, and
they conjectured N(s)=O_ε(s^{1+ε}). We verified the interval construction and
the equivalence directly.</p>

<p><strong>A clean reduction to one missing theorem.</strong> Pick two anchors
a₁,a₂∈A and set D=a₁+a₂. For every other a, the two numbers
x_a=(a+a₁)/D and y_a=(a+a₂)/D lie in the rank-s multiplicative group Γ_S
generated by S (all three sums are S-smooth), and x_a−y_a=(a₁−a₂)/(a₁+a₂) is a
fixed nonzero constant. The map a↦(x_a,y_a) is injective. So if U_2(s) is the
maximum number of solutions to a binary S-unit equation αx+βy=1 over any
rank-s subgroup of ℚ×, then <strong>N(s)≤2+U_2(s)</strong>: one uniform
subexponential estimate U_2(s)=exp(o(s)) would prove #126 outright. This is an
unusually tight reduction — we checked the logic and the injectivity.</p>

<p><strong>Why every existing S-unit bound stops exactly at log n.</strong> The
best explicit binary S-unit bounds (Hirata-Kohno–Kawashima–Poëls–Washio) are
exponential in the number s of places — over ℚ they give N(s)&lt;2+21·45^{s+1},
which recovers only f(n)≫log n, and with a worse constant than the elementary
argument. The dependence on s is the whole issue, not the constants. And a
polynomial U_2(s) is impossible: Konyagin–Soundararajan (and Ha–Soundararajan)
built s-prime sets with exp(s^β) solutions to a+b=c for β&lt;2−√2. Those lower
bounds are subexponential, perfectly compatible with what #126 needs — so the
naive route lands precisely on the open question: is the number of binary
S-unit solutions over ℚ uniformly exp(o(s))? We found no theorem giving that.</p>

<p><strong>The key structural point: stars versus cliques.</strong> A binary
S-unit equation only controls connections to TWO anchors. If u+1=v has many
S-smooth solutions, then a=u−1 connects smoothly to both anchors 1 and 2 — but
two such leaves a_i,a_j have a_i+a_j=u_i+u_j−2, completely uncontrolled. Many
binary solutions build a large K_{2,m}, NOT a K_{m+2}. In the normalization
above, two leaves are mutually compatible exactly when
x_i+x_j−2a₁/D ∈ Γ_S — so after solving one binary equation, the x's must still
form a CLIQUE in a shifted S-unit graph. That extra structure is what a proof
has to exploit, and it's exactly what generic S-unit bounds don't see.</p>

<p><strong>Two precise missing theorems, and a modern theorem that almost
fits.</strong> The reduction points at a "prime-generated S-unit clique lemma":
if Γ≤ℚ× is generated by s rational primes and X⊂Γ has x+x′−η∈Γ for all distinct
x,x′∈X, then |X|=exp(o(s)). Equivalently, package the sums as the rank-≤2
matrix M_{ij}=a_i+a_j: its off-diagonal entries lie in Γ_S and it satisfies the
Alon–Solymosi rectangle condition (m_jj·m_ik−m_jk·m_ij=(a_j−a_i)(a_k−a_j)≠0).
Their rank theorem recognizes exactly this structure — but its quantitative
dependence still yields only rank M≥(log n/s)^c, i.e. n≤exp(O(s)). The
ingredients a proof should use are narrower than generic finite-rank groups:
the group is generated by actual rational primes, the entries are positive
integers, the matrix is symmetric, and it has the exact additive form a_i+a_j.</p>

<p><strong>The local route is provably dead (verified).</strong> The classical
1934 argument halves the set once per available prime, inherently capping it at
2^s. This isn't fixable locally: for any s odd primes p₁,…,p_s and any sign
vector σ∈{±1}^s, the Chinese remainder theorem gives an integer a_σ≡σ_j (mod
p_j); any two a_σ,a_τ differ in some coordinate j and so a_σ+a_τ≡0 (mod p_j) —
2^s vertices satisfy EVERY local cancellation condition. What fails is only the
cofactor introducing outside primes. We built this construction for s=3,4,5
(all 2^s vertices, every pair cancelling at a designated prime). So local
divisibility data alone cannot beat the logarithmic bound; a proof must use
complete smoothness of the quotient, simultaneously across many pairs.</p>

<p><strong>Verified explicit data.</strong> N(2)=4 exactly: A={1,7,17,47} with
S={2,3} gives six sums {8,18,24,48,54,64}, all 2,3-smooth, and the book bound
N(2)≤2²=4 closes it. Exact branch-and-bound searches (every construction
re-checked by integer factorization on our side) give f(14)≤8 (14 elements on
the primes {2,3,5,7,11,13,17,19}, all 91 pair sums smooth) and f(21)≤12 (21
elements on 12 primes, all 210 pair sums smooth). Bounded-height searches show
the best clique sizes growing roughly LINEARLY in s (5,6,8,10,…,21) with no
exponential pattern — mild evidence for the positive answer, but brutally
caveated: S-unit constructions can live at astronomical heights (a 10¹²-height
anchored search for s=3 found max clique 5), and small-prime supports need not
be optimal. This is weak evidence, not asymptotics.</p>

<p><strong>Where it leaves it — a precise open problem, not a vague one.</strong>
We did not prove f(n)/log n→∞ and found no exponential construction pointing
the other way. What we have is a sharpening: the conjecture is equivalent to a
uniform subexponential bound for binary S-unit equations over ℚ, but the real
target is narrower — a rank-two / clique bound for prime-generated groups. The
concrete next attack is common-neighborhood decay: bound the number of y∈Γ_S
with x_i+y−η∈Γ_S for t fixed vertices, hoping for subexponential-in-s once t
grows slowly (generic Subspace Theorem estimates worsen with t; the hope is the
shared one-dimensional variable y plus the rational-prime structure). The
published record appears unchanged at logarithmic order (a targeted-search
conclusion, not a guarantee — a literature pass would precede any
publication-grade claim). This problem resisted two earlier automated attempts
as a bare wall; the reduction and the obstruction are the first real structure
on it we've banked. Genuinely open.</p>
`,
    links: [
      { label: "GPT-5.6 Sol — strong partial: S-unit reduction + stars-vs-cliques + CRT obstruction (chat transcript)", url: "https://chatgpt.com/s/t_6a66e40656ec819197af551103628a55" },
      { label: "erdosproblems.com/126", url: "https://www.erdosproblems.com/126" },
    ],
  },
  {
    slug: "41-b3-density",
    problemNum: 41,
    title: "#41: strong partial — the exact parity wall between B₂ and B₃, plus a real conditional theorem",
    date: "2026-07-27",
    status: "partial",
    summary:
      "#41 asks whether every infinite B₃-set (all triple sums distinct) must " +
      "have its normalized counting function dip to zero: liminf A(x)/x^(1/3)=0. " +
      "It's known for every even order and open for odd. GPT-5.6 Sol found no " +
      "resolution — but a strong partial: (1) the exact reason the classical B₂ " +
      "method breaks at B₃, a parity wall (a B_h condition controls an h-variable " +
      "signed form, which can balance + and − only when h is even); (2) a real " +
      "conditional theorem — any B₃-set with positive critical density must have " +
      "logarithmic gap spikes, so #41 holds for every smooth-gap B₃-set; (3) the " +
      "sharp finite bounds 1 ≤ liminf R₃(N)/N^(1/3) ≤ limsup ≤ 1.51546…; (4) an " +
      "explicit construction hitting the critical exponent 1/3 at checkpoints " +
      "(but with liminf zero). Constants and citations re-verified on our side.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/41">erdosproblems.com/41</a>,
OPEN, $500). A B₃-set is a set of integers in which all triple sums
aᵢ+aⱼ+aₖ (repetition allowed) are distinct. Write A(x) for the counting
function of such a set. The question: must every infinite B₃-set have its
normalized density dip to zero along a subsequence — is
liminf A(x)/x^(1/3) = 0? For B₂ (Sidon sets) and every even order this
"logarithmic dip" is known; #41 is the odd-order case h=3, and it is open.</p>

<p><strong>We did not resolve it. The status check is unusually clean, and the
partial package is real.</strong> A brand-new primary source — Christian Táfula,
"Infinite Sidon-type sets for zero-sum linear forms"
(<a href="https://arxiv.org/abs/2607.20753">arXiv:2607.20753</a>, July 2026) —
recovers the full logarithmic dip for every even order through zero-sum linear
forms, and states explicitly that the corresponding problem for odd h remains
open. So #41 has not quietly been subsumed by a general B_h theorem; the
parity is genuinely the obstacle. We confirmed the paper and its author are
real, and re-derived the load-bearing constants and the proof structure below
on our side.</p>

<p><strong>The diagnosis: an exact parity wall, not a missing trick.</strong>
The classical B₂ argument is bare-bones: if a Sidon set had
liminf A(x)/√x &gt; 0 then aₙ ≪ n²; take ≍ log x geometrically separated
blocks, each of span O(N²) partitioned into O(N²/x) intervals of length x;
Cauchy–Schwarz forces ≫ x equal-difference pairs per block, the Sidon property
makes all those differences distinct, and log x blocks give ≫ x log x distinct
integers in [1,x] — impossible. The whole engine runs on one cancellation:
translate a block by t and the differences (a+t)−(b+t) = a−b don't move. For
B₃ the useful injective expression is a+b−c, and translating gives
(a+t)+(b+t)−(c+t) = a+b−c+t — the block location does NOT cancel, so the
differences scatter instead of accumulating. The Fourier version is the same
wall: the even-order integrand is a product of matched |F|² factors, nonnegative,
so each dyadic block keeps its major-arc contribution and the blocks add; the
B₃ form carries F(α)²·F̄(α) = F(α)|F(α)|², an uncontrolled phase with no
nonnegative blockwise lower bound to sum. The clean statement of the wall: a
B_h condition naturally controls a signed form in h variables, and such a form
can have equally many + and − variables only when h is even.</p>

<p><strong>A real conditional theorem that falls out anyway.</strong> The run
proves: if a B₃-set has positive critical density, liminf A(x)/x^(1/3) &gt; 0,
then it must have logarithmically superquadratic gap spikes —
limsup (aₙ₊₁−aₙ)/(n²log n) &gt; 0, hence limsup (aₙ₊₁−aₙ)/n² = ∞.
Equivalently, <strong>#41 has a positive answer for every B₃-set whose gaps are
smooth</strong> (aₙ₊₁−aₙ = o(n²log n)). The mechanism: positive density pins
aₙ between c·n³ and C·n³; a block-crossing count on the injective sums
aᵢ+aⱼ−aₖ then forces ≫ x·min(ξ,log x) distinct values into [−x,x] if the gaps
stay below n²log n/ξ with ξ→∞, contradicting |[−x,x]∩ℤ| = 2x+1. The honest
label: this is a direct synthesis of Li's finite-B₃ injectivity observation and
the block-crossing architecture in Táfula's gap theorem, not a novelty claim.
What it buys is genuine but not fatal: any counterexample must be dense
<em>despite</em> violent sparse discontinuities, not dense and regular.</p>

<p><strong>The finite theory is healthier than the infinite one.</strong> Let
R₃(N) be the largest B₃-subset of [1,N]. O'Bryant's construction gives
R₃(N) ≥ N^(1/3) − N^(7/40) for large N, so liminf R₃(N)/N^(1/3) ≥ 1. The best
verified upper constant combines White's B₃ bound with Rechnitzer's 2026
rigorous computation of the L²-autoconvolution constant ν₂
(<a href="https://arxiv.org/abs/2602.07292">arXiv:2602.07292</a>, "The first
128 digits of an autoconvolution inequality"), which encloses
ν₂² = 0.5746396071515195… to 128 decimal digits:</p>

<p style="text-align:center">1 ≤ liminf R₃(N)/N^(1/3) ≤ limsup R₃(N)/N^(1/3)
≤ (2/ν₂²)^(1/3) = 1.51546116978632…</p>

<p>We re-checked that last arithmetic directly: (2/0.5746396071515195…)^(1/3)
reproduces 1.51546116978632 to the displayed digits. The limit
R₃(N)/N^(1/3) is not known to exist.</p>

<p><strong>An explicit construction hits the critical exponent — but only at
checkpoints.</strong> A scale-separated gluing lemma (if A⊆[0,P] and B⊆[0,L]
are finite B₃-sets with 0∈B, then A ∪ (t + d·B) is B₃ for explicit d,t that
make the four triple-sum ranges disjoint) lets one glue generalized
Bose–Chowla blocks over 𝔽_{q³} into an infinite B₃-set with
limsup log A(x)/log x = 1/3 — the critical exponent itself — and in fact
A(N_k) ≥ N_k^(1/3)/(log N_k)^(o(1)) along infinitely many checkpoints, with the
normalized checkpoint density decaying as slowly as prescribed. The catch,
stated plainly: this construction has liminf zero. Right before each new block
the counting function is still tiny while the next block starts at a vastly
larger scale, so it produces enormous valleys. It does not refute #41; it lives
exactly through the loophole the gap proposition exposes (gigantic inter-block
gaps), and shows a proof of #41 can only force a sparse subsequence of dips,
never a uniform rate. The strongest genuinely uniform infinite construction is
Cilleruelo–Tesoro's
(<a href="https://arxiv.org/abs/1206.3087">arXiv:1206.3087</a>),
A(x) = x^(√5−2+o(1)) = x^(0.2360679…), far below the critical 1/3 — we
re-checked √5−2 = 0.2360679… as well.</p>

<p><strong>What's still open.</strong> Everything above is a bounded search, a
conditional theorem, or a status reduction; no uniform statement that every
infinite B₃-set dips was proved, and the remaining case — dense despite violent
sparse discontinuities — is exactly what the parity wall leaves open. The
finite-field search over 𝔽₅³ and 𝔽₁₁³ Bose–Chowla families found no anomaly
(a 32-element best diameter at q=5), but that is computation, not a theorem.
#41 stays open; what changed is that the obstruction now has a name (the
even/odd parity wall), a conditional positive result (smooth gaps ⟹ the dip),
and a sharp finite window [1, 1.51546…] around the unknown limiting constant.</p>
`,
    links: [
      { label: "erdosproblems.com/41", url: "https://www.erdosproblems.com/41" },
      { label: "GPT-5.6 Sol — strong partial: the parity wall + conditional dip theorem (chat transcript)", url: "https://chatgpt.com/s/t_6a66df3ea2d08191ba12069f120cd1a0" },
      { label: "Táfula, Infinite Sidon-type sets for zero-sum linear forms (arXiv:2607.20753, July 2026)", url: "https://arxiv.org/abs/2607.20753" },
      { label: "Rechnitzer, The first 128 digits of an autoconvolution inequality (arXiv:2602.07292)", url: "https://arxiv.org/abs/2602.07292" },
      { label: "Cilleruelo–Tesoro, Dense infinite B_h sequences (arXiv:1206.3087)", url: "https://arxiv.org/abs/1206.3087" },
    ],
  },
  {
    slug: "885-factor-difference-k5",
    problemNum: 885,
    title: "#885: strong partial — three near-miss families, from three sources, each prove exactly saturated",
    date: "2026-07-27",
    status: "partial",
    summary:
      "Erdős–Rosenfeld, open at k=5: do five integers exist sharing at least " +
      "five common factor-differences D(N)={|a−b| : N=ab}? The cases k=2,3,4 " +
      "are solved. We ran GPT-5.6 Sol on it and found no witness — but a " +
      "strong partial: a clean reformulation (a k=5 witness is exactly a 5×6 " +
      "square-additive rectangle, equivalently a K₅,₅ biclique), an " +
      "independent re-verification of the known k=3 (Guiduli) and k=4 " +
      "(Bremner) examples, and three separate proofs that three different " +
      "near-miss families are exactly saturated — Bremner's k=4 rectangle, " +
      "Choudhry's brand-new June-2026 5×3 family, and a community list of 71 " +
      "4×6 rectangles each admit no further row or column, all re-run on our " +
      "side. Honest gap: no global obstruction proved; a witness could lie " +
      "past every region searched.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/885">erdosproblems.com/885</a>,
OPEN, [Erdős–Rosenfeld], 0 claimed proofs). For a positive integer N, let
D(N) = {|a−b| : N = ab} be the set of differences between complementary
factor pairs of N. The cases k=2 (Erdős–Rosenfeld 1997), k=3 (Jiménez-Urroz
1999) and k=4 (Bremner 2019) are solved: there exist k integers whose
factor-difference sets share at least k common values. The open case is k=5 —
do five integers exist with at least five common factor-differences? A single
explicit witnessing 5-tuple, verified by direct computation, would settle it.</p>

<p><strong>We did not find a witness. This is a strong partial, not a solution
— and the honest reason it isn't a disproof is at the end.</strong> What came
out is a clean reformulation, an independent reconstruction of the known k=3
and k=4 examples, three separate proofs that three different near-miss
configurations are <em>exactly saturated</em> (cannot be extended by one more
row or column), and a large exact search. Every computation below was re-run
on our side with our own code, not just read.</p>

<p><strong>The reformulation, which makes the whole thing geometric.</strong>
d ∈ D(N) if and only if d² + 4N is a perfect square: if N = a(a+d) then
d²+4N = (2a+d)², and conversely any such square gives the factor pair back.
So a k=5 witness is exactly two sets A = {d₁²,…,d₅²} and B = {0, 4N₁,…, 4N₅}
for which every element of A+B is square — a 5×6 square-additive rectangle,
equivalently a K₅,₅ biclique in the difference-of-squares graph. The zero
column is the subtle part: the Erdős–Rosenfeld question is not a generic 5×5
square-sum problem but the stronger 5×6 one with a zero on one side and
squares on the other. We re-derived the equivalence and spot-checked it
directly.</p>

<p><strong>The known examples, reconstructed and re-verified by our own
divisor enumeration.</strong> For k=3, the Guiduli examples recorded in
Erdős–Rosenfeld: we confirmed
D(6,925,500) ∩ D(37,901,500) ∩ D(108,448,956) = {420, 3780, 14940, 76860},
plus a second reported triple, exactly. For k=4, Bremner's 2019 construction:
the four integers 26,128,575 / 291,722,431 / 561,117,375 / 713,526,975 with
common differences {126, 16110, 33390, 75390}; we reproduced the full
intersection and every d=126 factor pair N = a(a+126).</p>

<p><strong>The flagship negative result: saturation, proved three times
over.</strong> (1) <em>Bremner's k=4 rectangle is bi-maximal.</em> Exhaustive
divisor-pair enumeration — every b that could shift the four squares
126², 16110², 33390², 75390² to four more squares arises from a divisor pair
of one fixed difference, so the search is finite and complete, not a cutoff —
shows the only such b are 0 and the four 4Nᵢ: there is provably no fifth
integer sharing those four differences, and the intersection computation shows
no fifth difference shared by those four integers. We reproduced this
enumeration ourselves and got exactly {0, 4N₁, 4N₂, 4N₃, 4N₄}. This closes the
most literal "just append a fifth point to Bremner" strategy. (2) <em>Choudhry's
brand-new June-2026 family.</em> Ajai Choudhry's paper (INTEGERS #A66,
arXiv:2508.07806) constructs parametric 5×3 and 4×4 square-sum families — one
column short, and exactly the shape that matters here. Its displayed 5×3
example we verified (all 15 sums square) and then proved bi-maximal the same
way: no fourth column exists. (3) <em>A community list of 71 primitive 4×6
rectangles</em> — exactly one row short — which the run checked in full: all 71
satisfy their 24 square conditions and each is bi-maximal at its scale, and a
scaling search over ~4.9 billion rational fifth-row candidates (denominator
≤ 10,000) found none surviving all six columns. (Those 71 are honestly a
community list, not a classification.)</p>

<p><strong>The searches, all negative.</strong> Direct: every D(N) for
N ≤ 3,000,000, scanning the incidence graph for a K₅,₅ — no witness (the best
5-integer intersection found had size 3). Difference-space: fixing the smallest
common difference ≤ 160 and the fifth-smallest ≤ 50,000, with the five integers
entirely unbounded (every candidate N is still enumerable exactly from divisor
pairs) — about 156 million incidences processed, no witness. Compact 5×6:
min Nᵢ ≤ 3,000,000 with the other four unbounded — no witness, recovering a
known 4×6 rectangle as a positive control. Each of these strictly contains a
naive "search a bigger box of N" approach.</p>

<p><strong>What's still open — and why this is not a disproof.</strong> No
global Diophantine obstruction was proved. Every negative result above is a
bounded search or a saturation proof at a displayed scale; a witness could lie
beyond all the searched regions, or inside Bremner's full elliptic family
rather than his one displayed specialization (we proved the specialization
non-extendable, not the family). The repeated, independent bi-maximality —
Bremner, Choudhry, and all 71 audited rectangles rigid at their displayed
scales — reads less like ordinary search scarcity and more like the expected
dimension dropping sharply once the final row or column is imposed. But that is
a heuristic, not a theorem: one exceptional high-rank elliptic or higher-genus
specialization could still produce a k=5 witness. The problem stays open; what
changed is that the literal extension routes are now provably closed, and the
search space has a clean geometric name.</p>
`,
    links: [
      { label: "erdosproblems.com/885", url: "https://www.erdosproblems.com/885" },
      { label: "GPT-5.6 Sol — strong partial: saturation proofs + exact search (chat transcript)", url: "https://chatgpt.com/s/t_6a66d1ec30888191a134999228e106cd" },
      { label: "DeepMind formal-conjectures Lean statement of #885", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/885.lean" },
      { label: "Bremner, On a problem of Erdős related to common factor differences (IJNT 2019)", url: "https://www.worldscientific.com/doi/10.1142/S1793042119500581" },
      { label: "Choudhry, two sets whose sumset is all squares — the 5×3 / 4×4 families (arXiv:2508.07806)", url: "https://arxiv.org/abs/2508.07806" },
      { label: "Erdős–Rosenfeld, The factor-difference set of integers (Acta Arithmetica 1997)", url: "https://eudml.org/doc/206983" },
      { label: "Jiménez-Urroz, A note on a conjecture of Erdős and Rosenfeld (J. Number Theory 1999)", url: "https://www.sciencedirect.com/science/article/pii/S0022314X99924071" },
    ],
  },
  {
    slug: "708-valuation-cover-c4",
    problemNum: 708,
    title: "#708: Round 7 — c₁₀ = 2, and the general slope falls to 1/5",
    date: "2026-08-11",
    status: "in_progress",
    originatedByUs: true,
    summary:
      "Erdős and Surányi's 1959 paper defined a constant cₙ — how long an " +
      "interval, as a multiple of max(A), guarantees n picks whose product is " +
      "divisible by ∏A — proved c₂=1 and c₃=√2, and reported no bounds in " +
      "general for 67 years. Rounds 1–6 pinned c₄ through c₉ at 2 and proved " +
      "cₙ ≥ 2 for every n ≥ 4. Round 7 proves c₁₀=2. A nested Hall reduction " +
      "leaves finite two- and three-defect bipartite kernels. Fixed label blocks " +
      "repair every prime-power layer except K₂,₅, where an order-statistic gcd " +
      "certificate and a matching among interval multiples take over. At the " +
      "aligned endpoint, the corrected van Doorn–Li–Tang injection has one " +
      "controlled two-adic anomaly whose edges form a matching; the repair " +
      "certificates survive it and avoid the midpoint before that point is added " +
      "for M. This determines cₙ through n=10 and improves the general bound to " +
      "cₙ≤n/5+6/5. Two hostile audits found and rejected a flawed first aligned " +
      "draft, then independently cleared the replacement. The famous g(n)≤2n " +
      "conjecture stays open and untouched.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/708">erdosproblems.com/708</a>,
OPEN, a $100-or-1000-rupee reward). Given n integers A with largest element M,
let g(n) be the least number such that from <em>any</em> M consecutive integers
you can pick g(n) of them whose product is divisible by the product of all of A.
Erdős and Surányi (1959) proved g(n) ≥ (2−o(1))n and asked whether always
g(n) ≤ 2n — which would be tight. Gallai had already got g(2)=2 and g(3)=4.
The general upper bound is the open problem and we did not touch it.</p>

<p><strong>Round 7 (11 August): the ten-label threshold is exact.</strong>
The sibling sequence now begins</p>

<p style="text-align:center;font-size:1.2em"><strong>
c₂=1, c₃=√2, and c₄=c₅=c₆=c₇=c₈=c₉=c₁₀=2.</strong></p>

<p>The private-prime padding theorem from Round 3 already gives c₁₀≥2.
Round 7 proves the matching upper bound <strong>c₁₀≤2</strong>.</p>

<p><strong>Nested Hall defects.</strong> Let A contain ten distinct positive
integers, M=max(A), and I=(x,x+2M)⊂[0,∞). First suppose x∉Mℤ. The two-halves
injection again makes each a∈A the exact positive difference of a simple
bipartite edge whose endpoints are interval multiples of a. If its ten edges
have distinct endpoint representatives, they are already the required cover.
Otherwise take a minimal Hall-deficient edge set. If the remaining edges also
fail to match outside its neighborhood, the deficiency rises from one to two;
repeat once more and it rises to three. Bipartite capacity and minimum degree
then leave only two-defect kernels with 8, 9, or 10 edges and three-defect
kernels with 9 or 10 edges.</p>

<p><strong>The finite kernels.</strong> The eight- and nine-edge cases are the
hard graphs from Rounds 5 and 6. A ten-edge/two-defect kernel has eight active
vertices. Up to bipartite isomorphism there are ten types: three on a 3-by-5
bipartition and seven on 4-by-4. Each admits two disjoint four-edge blocks
P,Q such that every vertex-induced prime-power level contains at least as many
whole blocks as its edge/vertex excess. Charging missing copies of each prime
to those blocks builds repair factors r,s with</p>

<p style="text-align:center"><strong>
∏a<sub>e</sub> divides (∏v)rs,
&nbsp; r|a<sub>e</sub> for e∈P,
&nbsp; s|a<sub>e</sub> for e∈Q.
</strong></p>

<p>The three-defect kernels are K₃,₃, K₃,₄ with two edges removed, and
K₂,₅. The first two have three fixed four-edge repair blocks. The finite
classification has 54 minimal K₃,₄ deletion patterns; another 12
same-column patterns contain a K₃,₃ core but satisfy the same certificate and
were checked redundantly.</p>

<p><strong>Why K₂,₅ needs a different idea.</strong> Write its labels as
a<sub>ij</sub> and put q<sub>j</sub>=gcd(a<sub>1j</sub>,a<sub>2j</sub>).
Let R be the gcd of the ten triple products q<sub>i</sub>q<sub>j</sub>q<sub>k</sub>.
Prime by prime, the missing endpoint valuation is the sum of the three smallest
q<sub>j</sub>-valuations, exactly v<sub>p</sub>(R). Therefore</p>

<p style="text-align:center"><strong>
∏a<sub>ij</sub> divides L₁L₂R₁R₂R₃R₄R₅·R.
</strong></p>

<p>Any three q<sub>j</sub>'s cover R. A König-theorem argument finds three
distinct unused interval multiples of three of them. If such a matching did
not exist, a two-vertex cover would trap all remaining multiples in at most
two points. Since every q<sub>j</sub> divides |L₁−L₂|, counting the intervening
multiples reduces the obstruction to three small integer cases, each
contradicting the number of distinct labels divisible by the same factor.</p>

<p><strong>Placing the ordinary repairs.</strong> A factor supported on four
distinct labels is at most M/4 and has at least seven multiples in the open
interval. The only new collision possibility is that two such progressions
together occupy at most nine points. Then their steps must agree: otherwise
their ratio is at most 5/4 while their least common multiple is too large for
the required intersection inside length 2M. Equality makes the common factor
divide the union of the support blocks, producing many more interval multiples
and another contradiction. Hall therefore places every repair at a distinct
unused point.</p>

<p><strong>The aligned endpoint needed a real repair.</strong> When x∈Mℤ, put
b₀=x+M and remove M. The corrected van Doorn–Li–Tang construction draws nine
edges for the remaining labels entirely inside I∖{b₀}. Exact prime-power
support can fail only at one surplus two-adic level on certain symmetric
edges, and those exceptional edges form a matching. Deleting such a matching
from an endpoint-induced level leaves the Round-6 block certificates valid.
Because all nine labels are strictly below M, the interval-multiple counts
also have enough slack to choose every repair point away from b₀. The resulting
nine-point product covers ∏(A∖{M}); only then do we adjoin the fresh point b₀
to supply M.</p>

<p>This last order matters. Our first draft incorrectly allowed b₀ to cover
some smaller-label valuation and then counted the same valuation again for M.
One hostile audit found the explicit counterexample M=10, A={1,…,10}, with
the nine-point product on {1,2,3,4,6,7,9,10,12}. We rejected that draft,
preserved the counterexample in the audit bundle, and published only after two
independent audits cleared the corrected avoid-b₀ construction.</p>

<p><strong>Sharpness and the new slope.</strong> The lower-bound verifier now
uses six private primes at (u,v,w)=(101,103,107). Its exact valuation DP finds
minimum cover size 11 in the 20,805-point bad interval, the n=10 instance of
the padding family whose length ratio tends to 2. Thus c₁₀≥2 and c₁₀=2.</p>

<p>Subadditivity now uses blocks of ten. Writing n=10q+r and using the exact
values for 0≤r&lt;10 gives</p>

<p style="text-align:center"><strong>
cₙ≤2⌊n/10⌋+c<sub>n mod 10</sub>≤n/5+6/5.
</strong></p>

<p>The public bundle checks all 2,250 labelled new two-defect kernels, all 66
K₃,₄ deletion patterns, 279,936 K₂,₅ valuation vectors, 3,888 aligned
graph/exceptional-matching pairs, every K₃,₃ exceptional matching, more than a
million arithmetic-progression phases, and 48,048 literal small aligned
instances. The unbounded valuation conclusion comes from the written
prime-power proof, not from capped computation. This determines cₙ through
n=10 and leaves the parent conjecture g(n)≤2n completely open.</p>

<p><strong>Round 6 (11 August): three simultaneous defects repair too.</strong>
The sibling sequence now begins</p>

<p style="text-align:center;font-size:1.2em"><strong>
c₂=1, c₃=√2, and c₄=c₅=c₆=c₇=c₈=c₉=2.</strong></p>

<p>The private-prime padding theorem from Round 3 already gives c₉≥2. The
new result is the matching upper bound <strong>c₉≤2</strong>.</p>

<p><strong>The extra fact at nine edges.</strong> Let A contain nine distinct
positive integers, M=max(A), and I=(x,x+2M)⊂[0,∞). When x∉Mℤ, use the same
two-halves graph as Round 5: the edge for a joins the last a-multiple in the
left half to that point plus a in the right half. The edges are simple and
distinct. More importantly, because the label is exactly the difference of
its endpoints, for every prime power p<sup>k</sup>,</p>

<p style="text-align:center"><strong>
p<sup>k</sup>|a<sub>e</sub> iff p<sup>k</sup> divides both endpoints of e.
</strong></p>

<p>Thus every prime-power support is a <em>vertex-induced</em> subgraph. That
is stronger than merely knowing that an edge label divides its endpoints,
and it is what makes the third repair controllable.</p>

<p><strong>Why the graph list is finite.</strong> If Hall gives nine distinct
endpoints, we are done. Otherwise choose a minimal deficient edge set S.
As before, |N(S)|=|S|−1 and</p>

<p style="text-align:center"><strong>
∏<sub>e∈S</sub>a<sub>e</sub> divides
gcd(a<sub>e</sub>:e∈S)·∏<sub>v∈N(S)</sub>v.
</strong></p>

<p>If the remaining edges have distinct representatives outside N(S), those
representatives and N(S) use eight points, and one unused gcd-multiple repairs
the product. If they do not, Hall supplies a larger edge set U with
|N(U)|≤|U|−2. A bipartite capacity count forces |U| to be eight or nine.
Eight edges then occupy exactly six vertices and form one of Round 5's hard
graphs, K₂,₄ or K₃,₃−e. Nine edges occupy six or seven vertices: six forces
K₃,₃, while seven either contains an eight-edge hard core or is one of two
3-by-4 types.</p>

<p><strong>Hard core plus one edge.</strong> Round 5 supplies two repair factors
r and s for the core, each dividing a fixed four-label block. Choose an
endpoint y of the ninth edge outside the six core vertices. Since 4r≤M and
4s≤M, each factor has at least seven interval multiples. A two-set Hall
argument, strengthened by the overlap lemma below, chooses distinct r- and
s-multiples outside the seven used points. Together with y and the core they
cover all nine labels.</p>

<p><strong>The two seven-vertex graphs.</strong> A no-core graph has bipartition
3+4. On the four-vertex side its degrees are (3,2,2,2); the three incomplete
columns miss rows with multiplicities (1,1,1) or (0,1,2). In either type one
can partition the nine edges into fixed blocks P and Q of sizes four and five
so that every proper vertex-induced subgraph with positive edge/vertex excess
contains all of P or all of Q. The full graph has excess two and contains both.
Prime-power layer counting therefore constructs r,s with</p>

<p style="text-align:center"><strong>
∏<sub>e</sub>a<sub>e</sub> divides (∏<sub>v</sub>v)rs,
&nbsp; r|a<sub>e</sub> for e∈P, &nbsp; s|a<sub>e</sub> for e∈Q.
</strong></p>

<p>Hence 4r≤M and 5s≤M. The s-multiples leave at least two choices outside
the seven graph vertices, while r leaves at least one, so distinct repair
points exist.</p>

<p><strong>K₃,₃ and three factors.</strong> Pair its three rows and columns by
index. For i=1,2,3, let D<sub>i</sub> be the four-edge K₂,₂ left after deleting
row i and column i. A vertex-induced prime-power level has positive excess
only when it is K₂,₃ or K₃,₂ (excess one), or the full K₃,₃ (excess three).
Charge a one-unit deficit to the block indexed by the missing row or column;
at a full level charge all three blocks. Summing levels gives factors
d₁,d₂,d₃ such that</p>

<p style="text-align:center"><strong>
∏<sub>e</sub>a<sub>e</sub> divides (∏<sub>v</sub>v)d₁d₂d₃,
&nbsp; and d<sub>i</sub> divides all four labels in D<sub>i</sub>.
</strong></p>

<p>Each factor has at least seven interval multiples. Hall for their unused
multiple sets reduces to pairs and the triple. If two factors had only one
unused point between them, their full multiple sets would be the same
seven-point progression, forcing the factors equal; that common divisor would
divide the seven labels in the union of their blocks and would actually have
at least 13 interval multiples. If all three had only two unused points, every
pair of full multiple sets would have union at most eight. The following
overlap lemma makes all three factors equal, after which the common divisor
divides all nine labels and has at least 17 multiples. Both are contradictions.</p>

<p><strong>The overlap lemma.</strong> If two interval-multiple sets each have
at least seven elements and their union has at most eight, their steps d,e
must be equal. Each set having at most eight points forces d,e≥2M/9. Their
intersection has at least six points, so five lcm(d,e)&lt;2M. But distinct
steps have lcm(d,e)≥2min(d,e)≥4M/9, impossible.</p>

<p><strong>The aligned endpoint, with every case exposed.</strong> If x∈Mℤ,
put b₀=x+M. The corrected van Doorn–Li–Tang construction removes M and b₀
and gives a simple eight-edge graph for A∖{M}, entirely inside I∖{b₀}; add
b₀ at the end to cover M. If the eight edges match, use their endpoints. If
a minimal deficient set has size s=8, use its seven neighbors and a
gcd-multiple; at s=7 use its six neighbors, an outside endpoint of the last
edge, and the gcd-multiple; at s=6 use its five K₂,₃ vertices, two distinct
outside endpoints of the remaining edges, and the gcd-multiple. The only
collision cases are exactly the inherited six-vertex hard graphs.</p>

<p>All eight labels are now strictly below M. Thus for a one-factor repair,
sg≤M−1, so I contains at least 2s gcd-multiples: enough to avoid the seven
selected graph points and b₀. In a hard graph, 4r,4s≤M−1, giving at least
eight multiples of each factor. If their unused sets collapsed to one point,
r=s would divide all eight labels; 8r≤M−1 would then give at least 16
multiples. Hence the eight-point cover can always avoid b₀, and adding b₀
finishes the aligned case.</p>

<p><strong>Sharpness, slope, and audit.</strong> The public padding verifier now
exercises r=5 explicitly: at (u,v,w)=(101,103,107), with private primes
10427, 10429, 10433, 10453 and 10457, its exact valuation DP finds minimum
cover size 10 in the 20,805-point bad interval. Thus c₉≥2 and c₉=2.</p>

<p>Subadditivity now uses blocks of nine. Writing n=9q+r and the exact values
for 0≤r&lt;9 gives</p>

<p style="text-align:center"><strong>
cₙ≤2⌊n/9⌋+c<sub>n mod 9</sub>≤2n/9+10/9.
</strong></p>

<p>Two independent hostile audits reconstructed the primary-source injection,
the graph classification, the arbitrary prime-power layer argument, the
three-factor placement, and all aligned endpoint counts. Their separate
checkers covered 1,572,864 seven-vertex valuation cases, 117,649 K₃,₃
valuation vectors, both inherited hard graphs, 22,620 small arithmetic phases,
2,731 literal interval instances, and the exact n=9 lower obstruction. No gap
or counterexample was found. This determines the sibling constants through
n=9; it still says nothing about the parent conjecture g(n)≤2n.</p>

<p><strong>Round 5 (11 August): the second Hall defect also repairs.</strong>
The sibling sequence now begins</p>

<p style="text-align:center;font-size:1.2em"><strong>
c₂=1, c₃=√2, and c₄=c₅=c₆=c₇=c₈=2.</strong></p>

<p>The Round-3 padding theorem already gives c₈≥2. The new result is the sharp
upper bound <strong>c₈≤2</strong>.</p>

<p><strong>The two-halves graph.</strong> Let A contain eight distinct positive
integers, M=max(A), and I=(x,x+2M)⊂[0,∞). First suppose x∉Mℤ. Split I at
x+M. For each a∈A, let u<sub>a</sub> be its largest multiple in the left half
and draw the edge (u<sub>a</sub>,u<sub>a</sub>+a) across the split. Both endpoints
are positive interval multiples of a. The eight edges are distinct because
their differences are the eight distinct labels a, so this is a simple
bipartite graph H.</p>

<p><strong>Why only two graphs are hard.</strong> Regard the edges as the left side
of an incidence matching problem and their endpoints as the right side. If
this graph satisfies Hall, choose one distinct endpoint for every edge; those
eight points already cover ∏A. Otherwise choose a minimal Hall-deficient set
S. It has |N(S)|=|S|−1 and obeys the Round-4 repair
identity</p>

<p style="text-align:center"><strong>
∏<sub>e∈S</sub>a<sub>e</sub> divides gcd(a<sub>e</sub>:e∈S)·∏<sub>v∈N(S)</sub>v.
</strong></p>

<p>No simple bipartite graph with at most five edges can be deficient, since
s&gt;⌊(s−1)²/4⌋ for 1≤s≤5. Thus |S| is 6, 7 or 8. The one-gcd repair works
immediately unless the whole eight-edge graph has exactly six active vertices:
at size 7 the last edge otherwise supplies a new endpoint; at size 6 the
obstruction is K₂,₃, and its two remaining edges have distinct outside
representatives unless the full vertex set again has size six. An eight-edge
simple bipartite graph on six active vertices is necessarily</p>

<p style="text-align:center"><strong>K₂,₄ or K₃,₃ minus one edge.</strong></p>

<p><strong>The two-factor lemma.</strong> In either hard graph, partition the eight
edges into fixed four-edge blocks P<sub>1</sub> and P<sub>2</sub>. For K₂,₄,
pair the four columns. For K₃,₃−e, put the two edges at the degree-2 left
vertex in P<sub>1</sub>, the two edges at the degree-2 right vertex in
P<sub>2</sub>, and split the central K₂,₂ two-and-two.</p>

<p>Fix a prime p. At level k, let H<sub>k</sub> contain the edges whose labels
are divisible by p<sup>k</sup>, and let V(H<sub>k</sub>) mean its incident,
non-isolated vertices. Those vertices are all divisible by p<sup>k</sup>, so
the endpoint product misses at most</p>

<p style="text-align:center"><strong>
δ<sub>k</sub>=max(0, |E(H<sub>k</sub>)|−|V(H<sub>k</sub>)|)
</strong></p>

<p>copies of p at that level. In K₂,₄, positive excess means exactly three
complete columns (δ=1) or all four (δ=2). In K₃,₃−e, it means the graph with
one further edge deleted, one of its two K₂,₃ subgraphs (δ=1), or the full
graph (δ=2). In every δ=1 case one fixed four-edge block is wholly present;
charge the missing copy of p to that block. In a δ=2 case charge one to each.</p>

<p>Let α<sub>p</sub> and β<sub>p</sub> count the levels charged to
P<sub>1</sub> and P<sub>2</sub>, and define
r=∏p<sup>α<sub>p</sub></sup>, s=∏p<sup>β<sub>p</sub></sup>. A charge to a
block occurs only at a level supporting all four of its edges, so
α<sub>p</sub>≤min<sub>e∈P₁</sub>v<sub>p</sub>(a<sub>e</sub>) and similarly
for β<sub>p</sub>; there is at most one charge to either factor at one level.
Thus r divides all four P<sub>1</sub> labels and s divides all four
P<sub>2</sub> labels. Since the six active vertex values are distinct, layer
summation gives, for every p,</p>

<p style="text-align:center"><strong>
Σ<sub>e</sub>v<sub>p</sub>(a<sub>e</sub>)=Σ<sub>k</sub>|E(H<sub>k</sub>)|
≤Σ<sub>k</sub>|V(H<sub>k</sub>)|+α<sub>p</sub>+β<sub>p</sub>
≤Σ<sub>v</sub>v<sub>p</sub>(v)+v<sub>p</sub>(rs),
</strong></p>

<p>and hence</p>

<p style="text-align:center"><strong>
∏<sub>e∈E(H)</sub>a<sub>e</sub> divides
(∏<sub>v∈V(H)</sub>v)·r·s.</strong></p>

<p><strong>Putting both repairs into the interval.</strong> Because each repair
factor divides four distinct labels at most M, 4r≤M and 4s≤M. Even with open
endpoints, the number of positive d-multiples in I is
ceil((x+2M)/d)−floor(x/d)−1≥ceil(2M/d)−1, so I contains at least seven
multiples of each factor. Let R and S be the full interval sets of r- and
s-multiples, and put U<sub>r</sub>=R∖V(H), U<sub>s</sub>=S∖V(H). Both are
nonempty. Hall for these two sets fails only if U<sub>r</sub>=U<sub>s</sub>={z}.
In that event R and S each have at least seven elements but lie in the same
seven-point set V(H)∪{z}; hence both equal it. Their sorted adjacent elements
differ by both r and s, forcing r=s. But r would then divide all eight labels,
giving 8r≤M and at least 15 r-multiples in I, a contradiction. Thus distinct
unused multiples of r and s exist, and with the six graph vertices they form
the required eight-point cover.</p>

<p><strong>The aligned endpoint.</strong> If x∈Mℤ, put b₀=x+M. The corrected
van Doorn–Li–Tang injection removes M and b₀, then gives the other seven
moduli seven distinct two-endpoint edges avoiding b₀. For a&lt;M it uses
(u<sub>a</sub>,u<sub>a</sub>+a) when a∤b₀,
(b₀−2a,b₀+2a) when 2a&lt;M and 2a∤b₀, and
(b₀−a,b₀+a) otherwise. Their paper proves the three types cannot collide.
Apply the one-defect repair to this seven-edge incidence graph, choosing its
gcd-multiple away from b₀, then add b₀ itself to cover M. The open-interval
count leaves at least eleven candidates in the smallest case, against only
seven forbidden points.</p>

<p><strong>Sharpness and the new slope.</strong> The private-prime padding
construction from Round 3 gives c₈≥2 uniformly; a concrete n=8 instance at
(u,v,w)=(101,103,107) has exact minimum cover 9. Therefore c₈=2. By
subadditivity, write n=8q+r with 0≤r&lt;8 and use the now-known exact constants
for r:</p>

<p style="text-align:center"><strong>
cₙ≤2q+c<sub>r</sub>≤n/4+1.</strong></p>

<p>Thus c₉ is now the first unresolved sibling value, with 2≤c₉≤3.</p>

<p><strong>Audit.</strong> Three hostile proof passes independently reclassified
the hard level subgraphs and checked the aligned construction against the
primary source. The finite checker exhausts all 256 support subgraphs and all
4⁸ valuation vectors through level 3 for each hard graph. The support
exhaustion checks the combinatorial classification; the written layer argument,
not the bounded valuation loop, covers arbitrary valuations. A separate probe
rebuilds van Doorn–Li–Tang's sharp six-neighbor K₂,₄ construction; its six
endpoints already cover all eight moduli, consistent with the theorem.</p>

<p><strong>Round 4 (11 August): the first two Hall defects are repairable.</strong>
The sibling constants, understood as infima of admissible scale factors so that
endpoint attainment does not change their values, now satisfy</p>

<p style="text-align:center"><strong>c₂ = 1, c₃ = √2, and c₄ = c₅ = c₆ = c₇ = 2.</strong></p>

<p>The lower bounds for the last four values come from the Round-3 theorem
cₙ ≥ 2 for every fixed n ≥ 4. The new work is the other direction:</p>

<p style="text-align:center;font-size:1.2em"><strong>c₆ ≤ 2 and c₇ ≤ 2.</strong></p>

<p><strong>The matching input.</strong> For A with M = max(A), join a ∈ A to
the positive integers b in an interval I when a divides b. Van Doorn, Li and
Tang prove that every open interval of length 2M has a matching of size
f(m) = min(m, ⌈2√m⌉) for every m-element A. Thus every set of at most five
moduli matches completely, and every seven-element set has a matching of size
at least six. For a smaller subset S ⊂ A, apply their theorem inside a
subinterval of I of length 2·max(S). Passing to the interior handles closed or
half-open endpoint conventions.</p>

<p><strong>The one-defect repair lemma.</strong> Suppose S is inclusion-minimal
among the sets that fail Hall, and write N(S) for its full neighborhood. Every
S\{a} matches, so |N(S)| = |S|−1 and each such matching is onto N(S). Put
g = gcd(S). Then</p>

<p style="text-align:center"><strong>∏<sub>a∈S</sub>a divides
g·∏<sub>b∈N(S)</sub>b.</strong></p>

<p>The proof is one line per prime. Fix p, remove an a<sub>p</sub> minimizing
v<sub>p</sub>(a), and match the other |S|−1 elements onto N(S). The matched
points supply all the valuations from S except v<sub>p</sub>(a<sub>p</sub>), while
v<sub>p</sub>(g) = v<sub>p</sub>(a<sub>p</sub>) supplies the missing valuation.
The matching may depend on p; the fixed product over N(S) does not.</p>

<p><strong>Six moduli.</strong> If A itself has no matching, no proper subset
can be deficient, so N(A) has exactly five points. Apply the lemma. The six
distinct elements of A are multiples of g = gcd(A), hence M ≥ 6g. Even an open
interval of length 2M contains at least ⌈2M/g⌉−1 ≥ 11 positive multiples of g.
Choose one z outside N(A). The six-point set N(A)∪{z} covers ∏A.</p>

<p><strong>Seven moduli.</strong> A minimal deficient S has size six or seven.
If |S|=7, repair it exactly as above. If |S|=6, let a₀ be the remaining
modulus. The six-matching theorem forces a₀ to have a neighbor y outside
N(S): otherwise all seven moduli together would have only the five neighbors
of S. Choose y first, then choose a g-multiple z outside N(S)∪{y}. Now
N(S)∪{y,z} has seven distinct points; z repairs S and y covers a₀.</p>

<p><strong>Sharpness and the new general bound.</strong> Round 3 already proved
cₙ ≥ 2 for every n ≥ 4, so the two upper bounds give c₆ = c₇ = 2. Also
c<sub>r+s</sub> ≤ c<sub>r</sub>+c<sub>s</sub>. To avoid assuming that an
infimum is attained, take any ε&gt;0, split an interval of length
(c<sub>r</sub>+c<sub>s</sub>+ε)M into two disjoint open blocks slightly longer
than c<sub>r</sub>M and c<sub>s</sub>M, cover the two parts of A separately,
and let ε decrease to zero. Writing n=7q+r, with 0≤r&lt;7, and using</p>

<p style="text-align:center"><strong>(c₀,…,c₆)=(0,1,1,√2,2,2,2), &nbsp;
cₙ ≤ 2q+c<sub>r</sub> ≤ (2/7)n+6/7.</strong></p>

<p>At the end of Round 4 this left 2≤c₈≤3. The one-defect argument alone did
not close automatically: the matching theorem guarantees only six matches, so
two uncovered moduli can compete for the same outside point. Round 5 above
resolves exactly that two-defect collision.</p>

<p><strong>Audit and provenance.</strong> Three independent high-effort proof
passes converged on the same lemma; one additionally classified the elementary
six-edge bracketing obstruction as K₂,₃. A standard-library checker exhausts
382,096 small translated six-set instances, repairs all seven bracketing
failures, and rebuilds genuine five-neighbor c₆ and c₇ full-graph obstructions
from the matching paper. Separate capped-valuation programs return minimum
cover sizes seven and eight for the n=6 and n=7 lower constructions.</p>

<p>An unpromoted local note dated 31 July already contained essentially this
repair lemma and claimed c₆=c₇=2. Round 4 independently reconstructed and
red-teamed it; this is not a priority claim. As of 11 August the live #708
tracker listed no claimed proof and no current worker. Nothing here is a
solution of the main g(n) problem.</p>

<p><strong>Round 3 (1 August): c₅ = 2 — and the sequence has a floor.</strong>
The sibling constant now reads</p>

<p style="text-align:center"><strong>c₂ = 1, c₃ = √2, c₄ = 2, c₅ = 2, and cₙ ≥ 2 for every n ≥ 4.</strong></p>

<p>With the trivial pairing bound cₙ ≤ ⌈n/2⌉ that boxes every later constant into
[2, ⌈n/2⌉]. Erdős and Surányi reported "no good upper or lower bounds" for cₙ in
general; the floor is a general lower bound, which is the part of that sentence
we think is worth the most.</p>

<p><strong>Which half is ours — stated up front, because it matters.</strong>
The upper bound c₅ ≤ 2 is <em>not</em> a new theorem. It is a short corollary of
<strong>van Doorn, Li and Tang, "Optimal bounds for an Erdős problem on matching
integers to distinct multiples" (arXiv:2603.28636, 30 March 2026)</strong>, which
proves that any m-element set can be matched to distinct multiples inside any
interval of length 2·max(A) in f(m) = min(m, ⌈2√m⌉) places. Since ⌈2√5⌉ = 5, f(5)
= 5 is a <em>perfect</em> matching — five distinct integers, one multiple of each
element — which immediately gives the product divisibility. Note n = 5 is the last
n where this works: f(6) = 5 &lt; 6. That paper (which solves a different Erdős
problem, #650) was public four months before we touched this. Anyone holding it
gets c₅ ≤ 2 in a line, and we are not going to pretend otherwise.</p>

<p><strong>The five-line version, for people who don't want to cite a paper.</strong>
Take any 2M consecutive integers I = {t+1,…,t+2M} and set γ = t+M+½. For each
a ∈ A take the two consecutive multiples of a bracketing γ: ℓ_a = a⌊γ/a⌋ and
r_a = ℓ_a + a. Both are in I. Read {ℓ_a, r_a} as an edge of a bipartite graph
(left = below γ, right = above); all |A| edges cross the cut, and they are
distinct because their lengths are the distinct elements a. If k of these edges
met at most k−1 vertices, that simple bipartite graph would need k ≤ ⌊(k−1)²/4⌋
edges — false for every k ≤ 5, and first true at k = 6. So Hall's theorem gives a
system of distinct representatives for n ≤ 5. The counting dies exactly at six
(K₂,₃ is six edges on five vertices), which is the same place vDLT's f(m) leaves
the diagonal. We ran 60,000 random 5-element instances against this: zero
failures.</p>

<p><strong>The lower bound c₅ ≥ 2 is ours, and it does not come free.</strong>
It does <em>not</em> follow from c₄ = 2 by monotonicity — cₙ is not obviously
nondecreasing, since a larger n makes the set harder but also hands you more
picks. (c₃ = √2 &lt; 2 is the sequence going <em>down</em> before it goes up.) The
move is to take the Round-2 c₄ obstruction and pad it with a prime that is
deliberately useless. Choose primes u &lt; v &lt; w with a prime q in (uv, vw), and set</p>

<p style="text-align:center">A = {uv, v², uw, vw, q}, &nbsp; M = vw.</p>

<p>Position by CRT (t ≡ 1 mod uw, t·uw ≡ v+1 mod v², t·uvw ≡ 1 mod q) an interval
of length 2uv−1 centred on x = tuvw. Inside it: x is the unique multiple of each
of uv, uw, vw and has exact (u,v,w)-valuation (1,1,1); x−v is the unique
v²-multiple and there is no v³-multiple at all; x−1 is the unique q-multiple and
is ≡ −1 mod u, v and w, so it contributes <em>nothing</em> to the rest of the
product. Every point other than x is divisible by at most one of u, v, w — any
second colour would be another multiple of uv, uw or vw.</p>

<p>Now count. ∏A = u²v⁴w²·q. Ignore q first. If you skip x, single-colouring
forces one point for u, one for w, and — since the only v²-multiple has valuation
exactly 2 and there is no v³ — at least three for v⁴ (best pattern 2+1+1). Five
points, all distinct. If you take x, it pays uvw and leaves uv³w, needing one u,
one w and two v points outside x. Five again. So <em>four points can never cover
u²v⁴w²</em>. And any five-point cover of the full product must burn one slot on
x−1 to get q, leaving four for the impossible core. Six picks are forced, while
|I|/M = (2uv−1)/(vw) = 2u/w − 1/(vw) → 2 as u/w → 1.</p>

<p><strong>We didn't trust the prose — we ran it.</strong> An exact
capped-valuation dynamic program (the genuine minimum cover, not a heuristic
search) returns <strong>6</strong> at (u,v,w,q) = (17,19,23,331), (29,31,37,907),
(41,43,47,1777) and (101,103,107,10427), with every uniqueness and neutrality
claim holding at each, and forcing ratios climbing 1.476 → 1.567 → 1.744 → 1.888.
The published certificate reproduces exactly: A = {323, 331, 361, 391, 437},
t = 14,257,816, x = 105,921,315,064, interval [105,921,314,742,
105,921,315,386], minimum cover 6.</p>

<p>The uniqueness conditions are not an artifact of small primes — they hold for
<em>all</em> u &lt; v &lt; w. The second v²-multiple sits outside the interval because
v(v−1−u)+1 &gt; 0 whenever v ≥ u+2, and the one below is out because u &lt; 1+v+1/v.
That is tight — the window has room for about 2u/v ≈ 2 of them and the CRT
placement is what keeps the count at one — but it is unconditional. For the
ratio to reach 2 we also need the primes to exist: three primes clustered tightly
enough, with a prime q in (uv, vw). Checked directly — (1009,1013,1019) gives
1.98037, (4133,4139,4153) gives 1.99037, (69481,69491,69493) gives 1.99965, and
(1865321,1865327,1865329) gives <strong>1.99999142</strong>, each with a genuine
prime q in range and all the uniqueness inequalities satisfied. No constant below
2 survives.</p>

<p><strong>The floor, which is the better theorem.</strong> The padding prime was
neutral by construction, so nothing stops you adding more. For n = 4+r, take r
primes q_j ∈ (uv+r, vw), park their unique multiples at x−1, …, x−r, and choose
u &gt; r so they stay neutral. An n-point cover spends r slots on inert points and
has four left for a core that needs five. Hence <strong>cₙ ≥ 2 for every fixed
n ≥ 4</strong> — permanently, for all n at once. Verified by the same exact DP:
minimum cover 7 at n=6 for (41,43,47) and (101,103,107), and 8 at n=7 for
(101,103,107), at ratio 1.888. At the time this did not determine cₙ for n ≥ 6;
Round 4 above now determines the first two values. The padding argument rules
out forever that any later constant dips below 2.</p>

<p><strong>What we are not claiming, and one live risk.</strong> Our targeted
search found no prior determination of c₅ and no published cₙ for n ≥ 4, and the
tracker still described the constants as having no good bounds in general — but
search-negative is a coverage claim, not a priority proof. At Round 3 publication
Wouter van Doorn, lead author of the matching paper, was listed as currently
working on #708. As of the Round 4 live check on 11 August that marker is None.
Round 4 also checked the 1959 primary PDF. The new repair lemma is not
Lean-formalized. And per that forum's own stated bar, "an AI verified it" is not
sufficient for posting, so we have not posted this there.</p>

<p><strong>Round 2: c₄ = 2, proved — and our Round-1 guess was
wrong, which is the better outcome.</strong> Round 1 (below) proved √2 ≤ c₄ ≤ 2
and then guessed that √2 was the sharp value — that the upper bound would come
down to meet the lower. <strong>That conjecture is false.</strong> A follow-up
found a different obstruction showing the upper bound is the sharp one:</p>

<p style="text-align:center;font-size:1.25em"><strong>c₄ = 2.</strong></p>

<p>The construction is a small but lethal modification of the √2 one. Where
Round 1 used A={w, uv, uw, vw}, take instead <strong>A={uv, v², uw, vw}</strong>
— the Erdős–Surányi c₃ triangle {uv, uw, vw} with the square v² added as the
fourth element. For primes u&lt;v&lt;w, place (by CRT: t≡1 mod uw and tuw≡v+1 mod
v²) an interval of length 2uv−1 around x=tuvw in which x is the unique multiple
of uv, uw and vw, x−v is the unique multiple of v², and there is no multiple of
v³. Then ∏A = u²v⁴w², and a clean 0/1 capacity count shows four picks can never
cover it: omit x and the single-colored points force one slot for u², one for w²,
and at least three for v⁴ (best pattern 2+1+1) — five slots; take x and the
residual u·v³·w needs four slots in the three remaining. Meanwhile the ratio
(2uv−1)/(vw) = 2u/w − 1/(vw) tends to <strong>2</strong> as the primes cluster.
We verified this decisively: an exact capped-valuation dynamic program returns a
minimum cover of exactly 5 for (u,v,w)=(17,19,23), (29,31,37), (41,43,47),
(101,103,107) — forcing ratios 1.476 → 1.567 → 1.744 → 1.888 — and an exhaustive
search confirms no 4-cover at the concrete (17,19,23) instance. Combined with the
Round-1 pairing upper bound c₄≤2, this gives c₄=2.</p>

<p><strong>Why √2 was the wrong guess, honestly.</strong> The Erdős–Surányi
c₃=√2 proof balances two competing thresholds — a "second pair-multiple"
threshold 2uv against a "square-repair" threshold w² — and their geometric mean
gives √2. The Round-1 c₄ construction inherited that balance. But adding v² to
the set <em>taxes</em> the square-repair point: the interval has exactly one
v²-multiple and no v³-multiple, so the formerly-free square repair now supplies
only half the v⁴ demand and no longer closes the cover. The square branch
disappears, the obstruction survives all the way out to the 2uv threshold, and
the normalized ratio is 2u/w → 2. The √2 lower bound we proved is still TRUE — it
is simply not sharp; c₄ sits at the upper bound, not the lower. Both Round-1
bounds were correct, and we guessed wrong about which was tight.</p>

<p><strong>Round 1: the sibling constant, and the first bounds past n=3.</strong>
The same paper asked a sharper quantitative version: how long must the interval
be — as a multiple cₙ of M — so that n picks <em>always</em> suffice? They
proved c₂=1 and c₃=√2, and then, in the tracker's own words, had "no good
upper or lower bounds in general." We prove</p>

<p style="text-align:center;font-size:1.25em"><strong>√2 ≤ c₄ ≤ 2.</strong></p>

<p>As far as the tracker shows, these are the first nontrivial bounds on any cₙ
beyond n=3.</p>

<p><strong>What c₄ ≥ √2 means, and the construction.</strong> There are
4-element sets A for which intervals of length approaching √2·M still force a
fifth pick. The construction is the n=4 analog of Erdős–Surányi's own c₃=√2
trick: take primes u&lt;v&lt;w with 2uv&lt;w², set A={w, uv, uw, vw} so M=vw, and
position (by the Chinese remainder theorem) an interval of length 2uv−1 whose
centre x is the unique multiple of uv, uw and vw inside it, with no multiple of
w² inside at all. Then every pick carries at most one factor w, so three
w-multiples are forced, and none of the remaining picks can supply both u and v
— four picks cannot reach u²v²w³ = ∏A. As u,v,w scale with w≈√2·u the ratio
(2uv−1)/(vw) tends to √2.</p>

<p><strong>We didn't trust the prose — we ran it.</strong> We instantiated this
with real primes at five scales and ran an exact dynamic program over capped
prime-valuation states, which computes the genuine minimum cover rather than
searching heuristically. Every instance forces exactly five picks, all the
uniqueness claims hold, and the forcing ratio climbs 1.382 → 1.391 → 1.402 →
1.410 → 1.411 toward √2 = 1.4142… from below. Since "no 4-cover works" is
inherited by every sub-interval, that certifies c₄ ≥ √2 against the page's
exact definition of cₙ.</p>

<p><strong>The upper bound c₄ ≤ 2 is almost embarrassingly clean once seen.</strong>
Split any interval of length 2M into two disjoint M-blocks. In the first, apply
g(2)=2 to two of the four integers; in the second, apply it to the other two.
Four picks total, product divisible by ∏A. We verified g(2)=2 exhaustively —
every pair at small sizes, every interval position: maximum cover exactly two,
and some pairs genuinely need two — and ran 300 random 4-integer tests on
2M-intervals, every one of which had a 4-cover. Hence √2 ≤ c₄ ≤ 2.</p>

<p><strong>Two things we are explicitly not claiming.</strong> First, the
lower-bound mechanism is not ours: it is the n=4 specialization of Erdős and
Surányi's 1959 c₃=√2 construction, reconstructed independently here, and we
name it as theirs — what was new in Round 1 was applying it to c₄ for the lower
bound; Round 2's new contribution is the v² obstruction proving c₄=2 (and showing
the √2 lower, while true, is not sharp). Second, "apparently new" is not "proved
first-ever": the tracker listing no general bounds is strong evidence that c₄ in
particular had never been pinned down (our targeted search found no later
determination of c₄ either), but a full reading of the 1959 paper and its
follow-ups is still ahead of us, and we say so rather than overstate.</p>

<p><strong>And g(4) itself.</strong> We confirmed g(4) ≥ 5 with the same exact
machinery — a clean witness: A={13, 77, 91, 143}, interval [5935, 6077], where
no four picks work and five do — but that is the paper's own n+1 lower
construction, not new. The reasoner also floated a weak g(4) ≤ 24 without proof;
we do not assert it. The honest conjecture is g(4)=5, and it is open.</p>

<p><strong>Where it stands now.</strong> The sibling constant is determined
through n=8: <strong>c₂=1, c₃=√2, and c₄=c₅=c₆=c₇=c₈=2</strong>. Pairing still gives
cₙ≤⌈n/2⌉, but c₅=2 already shows it is not generally sharp. Round 5 improves
the general upper bound to cₙ≤n/4+1 by subadditivity. Together with the
permanent floor cₙ≥2, this leaves c₉ as the first exact value: 2≤c₉≤3. The
parent problem g(n)≤2n remains open and untouched; the reasoner's clean
diagnosis of why the naive fractional covering argument cheats (it drops the
"use each integer at most once" capacity constraint, where the difficulty
lives) still stands.</p>
`,
    links: [
      { label: "GPT-Pro Round 3 — c₅=2 and the cₙ≥2 floor (chat transcript)", url: "https://chatgpt.com/s/t_6a6d58a716b881918308c93de23fc91d" },
      { label: "van Doorn, Li, Tang — arXiv:2603.28636 (the upper bound is a corollary of this)", url: "https://arxiv.org/abs/2603.28636" },
      { label: "Verification code — c₆ through c₁₀ repairs, independent graph-layer audits, exact lower-bound DP", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/708" },
      { label: "Erdős–Surányi 1959 primary PDF", url: "https://users.renyi.hu/~p_erdos/1959-07.pdf" },
      { label: "GPT-Pro Round 2 — c₄=2, the v² obstruction refuting c₄=√2 (chat transcript)", url: "https://chatgpt.com/s/t_6a66ea42150c8191a20d421c4e913a35" },
      { label: "GPT-Pro Round 1 — the c₄ bounds (chat transcript)", url: "https://chatgpt.com/s/t_6a66bfd37e588191a30384b719c11e06" },
      { label: "erdosproblems.com/708", url: "https://www.erdosproblems.com/708" },
      { label: "erdosproblems.com/709 (the matching sibling)", url: "https://www.erdosproblems.com/709" },
    ],
  },
  {
    slug: "349-beatty-completeness",
    problemNum: 349,
    title: "#349: Round 5 — a closed form, a cross-family proof, and a 1964 structure in disguise",
    date: "2026-07-26",
    status: "in_progress",
    summary:
      "Round 5 — the capstone. The 0-indexed entirely-complete boundary has a " +
      "closed form, t0(α) = min over k≥0 of (2^k+1)/α^k, now triply confirmed " +
      "(our exact-rational compute, a same-family skeptic, and a cross-family " +
      "GPT-5 Pro proof whose key move is Graham's 1964 Lemma 4 in disguise). " +
      "The honest payoff is provenance: under the reindex u=t/α the 0-indexed " +
      "sequence IS the literature's sequence, so for t<α we sit inside Graham's " +
      "1964 unit square (Acta Arithmetica 10, primary-verified — Lemma 1 the " +
      "greedy criterion, Theorem 5 the powers-of-two obstruction, Theorem 6 the " +
      "regions whose pullback is exactly our fragmented complete set, Theorem 3 " +
      "complete iff entirely complete there) and for t≥α inside van Doorn 2026. " +
      "So the set, its ≈85% area, and its region structure are Graham's; the " +
      "1-indexed closed thresholds are van Doorn's. What is genuinely new is the " +
      "independent cold re-derivation plus the one-line min-formula boundary of " +
      "Graham's set in 0-indexed coordinates (explicit shelf + least-minimizer) — " +
      "a unification not previously written — not a new theorem. We think that " +
      "is the better, truer story.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/349">erdosproblems.com/349</a>,
still shows OPEN, 0 claimed proofs). For which t, α ∈ (0,∞) is the
sequence s_n = ⌊t·αⁿ⌋ (n=1,2,3,...) "complete" — meaning every
sufficiently large integer can be written as a sum of distinct terms
from the sequence? The page notes this is open even restricted to
t ∈ (0,1).</p>

<p><strong>What's actually true: the vast majority of this problem is
already solved, in the open literature, uncredited on the tracker.</strong>
R.L. Graham's classical 1964 result (Acta Arithmetica 10, 63–70) fully
characterized the square 0&lt;t&lt;1, 1&lt;α&lt;2. What the tracker
doesn't reflect: Wouter van Doorn — the same person who separately
resolved Erdős #1005 this year — posted "Completeness of exponentially
increasing sequences" (arXiv:2602.23394, 25 February 2026), which
extends Graham's methods to settle the question almost everywhere. For
α∉[1,2]: never complete for any t. At α=1: complete iff t∈[1,2). At
α=2: complete iff t=1/2^j for integer j≥0. For φ≤α&lt;5^(1/3) (φ = golden
ratio ≈1.618): t &lt; min(3/α, 5/α²) is the <em>entirely-complete</em>
threshold, which equals the complete threshold there (so an iff on
that sub-range). For 1&lt;α&lt;φ the same expression min(2, 3/α, 5/α²)
is only a <em>sufficient</em> condition — t below it is entirely
complete hence complete — but it is NOT an iff: above it the sequence
can still be complete without being entirely complete, and that is
exactly the open region. <strong>Round 3 retraction:</strong> the "completely
solved for every α≥φ" line we carried through Rounds 1–2 was
over-stated — see the convention note below; on the problem as
formally posed the solved set is narrower than that.</p>

<hr>

<p><strong>Round 2, next day: a real correction to our own Round 1
formulas, made in the open — plus real new progress on the remaining
strip.</strong> We fired a follow-up brief asking a fresh reasoner to
push further into the open region using van Doorn's own machinery. It
came back and, in its own self-audit, flagged something we'd gotten
wrong the day before: "indexing is treacherous." It was right.</p>

<p><strong>The bug, plainly.</strong> Van Doorn's own paper indexes his
sequence starting at n=1 (first term ⌊tα⌋). Round 1's prose described
the sequence as starting at n=0 (first term ⌊t⌋) — and then quoted
van Doorn's threshold formulas verbatim, without adjusting for the
shift. The two sequences aren't the same object under a naive reading
of "t": van Doorn's own "t" corresponds to a different quantity than
what a reader following Round 1's "n=0,1,2,..." framing would compute.
We independently re-derived the correct translation twice — once by
hand, once via a fresh background verification pass — and both landed
on the same fix, now reflected above: the two min(...) thresholds each
pick up an extra factor of α, and the α=2 condition shifts from
requiring j≥1 to j≥0 (t=1 itself, previously excluded, is actually
fine — verified directly: t=1/8 stays gap-free to N=2000, while t=2
and t=3/4 both show real, persistent, growing gap patterns, confirming
which side of the line each value is really on). Worse, Round 1's own
"we verified this by computation" paragraph turned out to be
silently checking van Doorn's sequence while claiming to check ours —
a real, if honest, mistake, not a fabrication. Re-run against the
corrected threshold: at α=1.65 the true cutoff is t≈1.818 (exactly
min(2, 3/1.65, 5/1.65²)) — t=1.80 and t=1.818 stay clean to N=6000,
t=1.83 develops the same geometric gap pattern Round 1 described, just
at the right place this time.</p>

<p><strong>The new progress: the entire line t∈[2,20] at α=3/2 is now
proven complete — not spot-checked, tiled.</strong> Using the same
bootstrap mechanism as van Doorn's own Lemma 5 (if a finite prefix's
subset sums already cover an interval as long as the next term, and
the sequence's growth rate has slowed enough, completeness propagates
forever), the run built an exact rational-arithmetic tiling of the
entire continuum t∈[2,20) into 49,674 cells, each with its own
explicit finite certificate. We couldn't reproduce the full tiling, but
we reproduced the mechanism from scratch and checked it at both ends
and in between: at t=20 specifically, we enumerated all 2¹⁹=524,288
subsets of the first 19 terms directly (not the fast bitset trick — a
genuinely independent method) and confirmed the interval [20505,68118]
really is fully covered, length 47,614, comfortably past the 44,336
needed. Spot-checked ~27 points across [2,20] including several
irrational-adjacent values; every single one bootstrapped cleanly.
This slice isn't in van Doorn's own published tables (which stop at
t≤50, α≤1.1) — it's new, though computer-assisted (rigor label (c),
not a hand proof) and doesn't touch t&gt;20 or the rest of the strip.</p>

<p><strong>Why we're doing this in public instead of quietly editing
Round 1.</strong> Same policy as the #1151 and #1063 corrections: a
mistake found and fixed the next day, named plainly, is worth more than
a silently-repaired paragraph. The underlying literature find (van
Doorn's real, uncredited paper) was never in question — only our own
transcription of it, which is now fixed and re-verified twice over.</p>

<hr>

<p><strong>Round 3 — the real find of the night isn't a new bound, it's
that the problem is two problems.</strong> We went to verify a fresh
GPT-Pro result (an extension of van Doorn's Proposition 8) against
van Doorn's actual PDF, and in doing so pulled a thread that unraveled
our own entry. The thread: erdosproblems.com/349 writes the sequence
as ⌊t·αⁿ⌋ and never pins where n starts. That looks like a typo-level
detail; it isn't. For t≥1 the n=0-indexed sequence (⌊t, ⌊tα⌋,
⌊tα²⌋, …) and the n=1-indexed one (⌊tα⌋, tα²⌋, …) are
<em>different</em> sequences with <em>different</em> completeness
answers — the extra leading ⌊t⌋ term can supply representable sums
that close gaps the other sequence has (at t=1, α=2 the 0-indexed
sequence is the powers of two from 1, hence complete; the 1-indexed
one is the powers of two from 2, which can never make an odd number).</p>

<p><strong>Who picks which convention.</strong> The official
machine-checked statement of the problem —
<a href="https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/349.lean">the
Lean formalization</a> the page displays as "Formalised: Yes" — defines
it as <code>range (fun n : ℕ ↦ ⌊t·αⁿ⌋)</code>, i.e. n∈ℕ, the
<strong>0-indexed</strong> sequence including ⌊t. Van Doorn's February
2026 paper — the one Rounds 1–2 leaned on as "solving α≥φ" — works
throughout with s₁=⌊tα⌋, the <strong>1-indexed</strong> sequence. So
do tonight's Pro result and its rectangle certificates (they reproduce
van Doorn's published rectangles exactly). The literature that
"solved" the solved part of #349 solved a one-index-shifted
<em>sibling</em> of the formally-posed problem.</p>

<p><strong>Our earlier entry lived in both conventions at once.</strong>
Its numerics — and the α=2 condition "t=1/2ʲ, j≥0" — are 0-indexed
(the formalized reading; we re-confirmed j≥0 directly: t=1,½,¼ clean
to 200,000, t=¾,1.5,2 gappy). But its "solved-map" prose, and the
α=1.65 thresholds it quoted, were read off van Doorn's 1-indexed paper
and silently shifted (van Doorn writes min(3/α², 5/α³); we had
min(3/α, 5/α²)) without ever saying the shift happened. The two halves
didn't agree, and the cleanest symptom needed no convention argument
at all: the entry was internally contradictory at α=3/2 — the iff-line
said complete requires t&lt;2, while the tiling-line in the same entry
said t=2…20 is complete. Root cause: "complete" (cofinitely many
representable) is not "entirely complete" (the threshold min(2,3/α,5/α²)
is the <em>entirely-complete</em> boundary, a one-way sufficient
condition for complete); on the open strip complete is strictly
larger. That iff is corrected above to a ⟹.</p>

<p><strong>On the formalized (0-indexed) problem the solved set is
narrower than "α≥φ done."</strong> Van Doorn's 1-indexed Proposition 3
("for 5^(1/3)≤α&lt;2, no t≥1 is complete") does <em>not</em> transfer:
at α=1.8, t=1 the 0-indexed sequence begins 1,1,3,5,… — the doubled
leading 1 closes exactly the small gaps the Corollary-1 permanent-gap
obstruction needs to fire — and we find no gap up to 200,000
(completeness there is still open, but it is decisively <em>not</em>
ruled out the way van Doorn rules it out on 1-indexed). So on the
problem as formally posed, parts of [5^(1/3),2) that are "never
complete" on the 1-indexed reading are open-or-complete on the
0-indexed one, and van Doorn's clean "α≥φ solved" map is a 1-indexed
statement. We have not mapped the exact 0-indexed solved boundary
inside [φ,2); we keep van Doorn's 1-indexed iff's as the reference and
flag the 0-indexed boundary as open. What we <em>do</em> stand behind
on 0-indexed, each directly checked: α=1 (iff t∈[1,2)); α=2 (iff
t=1/2ʲ, j≥0); the sufficient condition t&lt;min(2,3/α,5/α²); and the
α=1.65 wall sitting exactly at t=3/α≈1.818 (t=1.80, 1.818 clean to
60,000; t=1.82 gaps at 2).</p>

<p><strong>So tonight's Pro result is real — on the sibling.</strong>
We verified its machinery (Propositions 8 and 9, Lemmas 5 and 7) word
for word against the PDF and its computer-assisted certificate
(117,805 leaf rectangles extending the α≤1.4 frontier to α≤1.529 for
t≤3, with an independent replay) is sound <em>on the 1-indexed
reading</em>. But that reading's open strip is a differently-shaped
region from the 0-indexed one (the leading term moves it), so the
specific 1.529 does not transfer to the formally-posed problem without
re-running the tiling on the 0-indexed sequence — not done. We record
the Pro result here as progress on the 1-indexed sibling, not as
#349-as-formalized progress; folding it in as the latter would repeat
the exact convention-muddle we're now correcting. (Likewise the
Round-2 t∈[2,20] at α=3/2 tiling we keep is a 0-indexed
computer-assisted result — and is now correctly understood as a
complete-<em>but-not-entirely-complete</em> result living inside the
open strip, the very thing the old iff-line wrongly excluded; its
t=20 Lemma-5 certificate interval [20505,68118] re-confirms on the
0-indexed first-19 terms.)</p>

<p><strong>The honest state, restated.</strong> #349 as formally posed
(0-indexed) is more open than anyone's summary — including our own,
until tonight — said, precisely because the work that "solved" it
solved a one-index-shifted sibling. That's the real, genuinely
interesting output of verifying this link: not a new number, but a
map drawn against the right coordinates, with the convention fork
named so the next person doesn't fall into it (and so we don't, a
fourth time — we nearly "fixed" this entry toward the 1-indexed
reading before the Lean file stopped us).</p>

<hr>

<p><strong>Round 4 — the fork is a theorem, and it goes our way.</strong> We
re-ran the completeness question on the 0-indexed sequence the formalization
poses — s_n = ⌊t·αⁿ⌋ for n=0,1,2,…, with the leading ⌊t⌋ term — using a
from-scratch exact-rational verifier, and proved a theorem about it. First,
though, a correction in our own favor.</p>

<p><strong>Retracting a caution from Round 3.</strong> Above we said the Pro
result's α≤1.529 region "does not transfer to the formally-posed problem
without re-running the tiling." Too cautious, and we retract it: completeness
is monotone in the term set. The 0-indexed sequence is {⌊t⌋} ∪ {the 1-indexed
terms} — a superset — so any integer representable from the 1-indexed terms is
representable with the extra term unused. Every 1-indexed cofinite-completeness
result (van Doorn's rectangles, the Pro extension to α≤1.529) is therefore
<em>automatically</em> true of the 0-indexed sequence. The certificate doesn't
transfer; the truth does, for free. The real question is how much
<em>further</em> 0-indexed reaches — and that is what's new below.</p>

<p><strong>The theorem.</strong> Take 0-indexed s_n = ⌊t·αⁿ⌋ with 1&lt;α&lt;2 and
t≥1. Run the greedy: keep the largest C with every integer in [0,C] a subset
sum, start C=0, feed terms in increasing order; a term s extends to [0,C+s]
exactly when s ≤ C+1, and if ever s &gt; C+1 then C+1 is a permanent gap.
<strong>Claim: if the greedy clears the first M+1 terms with no gap — M being
the first n with f(n) = t·α^(n+1)·(2−α) − n·(α−1) − t ≥ 0 — then the sequence
is entirely complete: every positive integer is a sum of distinct terms.</strong>
(M exists because for α∈(1,2) the exponential t·α^(n+1)·(2−α) eventually beats
the linear n(α−1)+t.)</p>

<p><strong>The proof.</strong> By induction the covered interval is [0,C_n],
C_n = s_0+⋯+s_n, while each s_{n+1} ≤ C_n+1 (the interval and its translate
then merge). The greedy hypothesis gives this for n&lt;M. For n≥M we force it:
s_{n+1}=⌊t·α^(n+1)⌋ ≤ t·α^(n+1), while C_n = Σ⌊t·αᵏ⌋ ≥ t·(α^(n+1)−1)/(α−1) −
(n+1) (each floor drops less than 1). So s_{n+1} ≤ C_n+1 follows once
t·α^(n+1) ≤ t·(α^(n+1)−1)/(α−1) − n, which rearranges exactly to f(n) ≥ 0. And
f(n) ≥ 0 holds for <em>every</em> n≥M: f(n+1)−f(n) = (α−1)·[t·α^(n+1)·(2−α) − 1],
and f(n)≥0 already gives t·α^(n+1)·(2−α) ≥ n(α−1)+t ≥ t ≥ 1, so the bracket is
non-negative and f never dips back below zero. The interval grows forever,
C_n→∞, every positive integer is captured. ∎</p>

<p><strong>Ran, not just read.</strong> The verifier (<code>lab.py</code>, exact
Fractions throughout — no floating point in any proof-critical step) finds M,
checks the monotonicity, and runs the greedy base exactly. At (t,α)=(1, 9/5):
M=5, the greedy covers [0,38] gap-free, f(5)≈1.80≥0 and rising, so the sequence
is entirely complete — independently confirmed by a from-scratch subset-sum
bitset representing every integer in [1,300,000] with zero gaps. The checker was
validated before trust: it reproduces the known α=1 (complete iff t∈[1,2)) and
α=2 (iff t=1/2ʲ, j≥0) cases exactly, and the α=1.65 1-indexed gap structure
Round 2 measured. An independent adversarial review then re-derived the algebra
(confirming the floor accounting term-by-term), proved the monotonicity, and ran
its own counterexample search — 47 certified points cross-checked against direct
enumeration to N=250,000 and three to N=1,000,000, all gap-free; zero
counterexamples. It also noted the sustainment half is stronger than stated
(the monotonicity actually survives all t&gt;0; our t≥1 is conservative, the
fork living at t≥1 where ⌊t⌋=1).</p>

<p><strong>The frontier.</strong> Largest t that is provably entirely complete,
by α (0-indexed by this theorem vs the same notion 1-indexed):</p>

<pre style="font-family:'JetBrains Mono',monospace;font-size:0.85em;line-height:1.5;overflow-x:auto">
   α               1-indexed t_max    0-indexed t_max
   1.5                 1.330              1.990
   1.529 (Pro)         1.277              1.957
   φ ≈ 1.618           1.145              1.851
   1.7                 1.013              1.726
   5^(1/3) ≈ 1.71       — none —          1.706
   1.8                  — none —          1.541
   1.95                 — none —          1.165
</pre>

<p>(Boundary to a t-resolution of ~0.007; the certified region is a genuine
interval [1, t₀(α)] — verified monotone in t, so every value below a certified
point is certified too.) Two things. The 0-indexed region is larger
<em>everywhere</em> — the extra ⌊t⌋ term lifts the frontier from ~1.33 to ~1.99
at α=1.5. And the qualitative separation: <strong>the 1-indexed frontier pinches
off completely at α≈5^(1/3)≈1.71</strong> (van Doorn's Proposition 3 — no t≥1
complete there) <strong>while the 0-indexed entire-complete supremum T(α) stays positive all the way to α→2.</strong> Across the whole range α∈[1.71, 2), the sequence the literature
proved things about has no complete point at t≥1, and the sequence the problem
actually asks about is entirely complete on a nonempty top interval [t_min(α), T(α)) — equal to [1, T(α)) up to α≈1.87, then excluding t=1 above α=13^(1/4)≈1.899 and possibly fragmented above ≈1.87 (the original wording here overstated this as the whole interval [1, t₀]; see the errata below).</p>

<p><strong>One point, concretely.</strong> At (t,α)=(1, 1.8) the 0-indexed
sequence 1,1,3,5,10,18,34,… is entirely complete (certified, and directly
enumerated gap-free to 300,000). The 1-indexed sequence — same terms minus the
leading 1 — is not even cofinitely complete: the integers it fails to represent
in [1,N] number 1,290 at N=50,000; 2,007 at 100,000; 3,272 at 200,000; 4,848 at
400,000. The count keeps growing — about 1.2% of all integers permanently
missing, scattered forever (a "covered tail" near the top of any finite window
is an artifact; the gaps recur above it). One leading ⌊t⌋=1 term fills every
one of those ~1.2% of gaps. That is the convention fork, measured.</p>

<p><strong>In the strip 1&lt;α&lt;φ</strong> the Lemma-5 cofinite certificate
also fires on the 0-indexed sequence, including non-trivially ((t,α)=(5/2,3/2)
certifies at r=7 with a subset-sum interval of length 69 ≥ next term 64) —
consistent with, and by monotonicity strictly containing, the 1-indexed
certificates. The new content is not in the strip but in [φ,2), where Lemma-5
propagation stops working and the greedy-sustainment theorem above carries.</p>

<p><strong>Honest calibration.</strong> This is a proof, not a formalization —
not Lean/Coq/Isabelle. The analytic part is short enough to read directly (it's
reproduced in full above) and every proof-critical computation is exact rational
arithmetic, replayable from the linked code. A follow-up round found the closed form: <strong>T(α) = min over k≥0 of (2ᵏ+1)/αᵏ is the exact supremum of the entire-complete t's</strong> (confirmed to 8·10⁻²⁸ over an adversarial α-set; the powers-of-two greedy prefix 1,2,4,…,2^{k−1} at the boundary is what makes the formula exact). The original wording here overstated the region as the interval [1, t₀(α)] with completeness for all t≤t₀ — that is wrong: entire-completeness is not monotone in t (for α≳1.87 the set can be disconnected, and t=1 stops being entire-complete above α=13^(1/4)≈1.899). Correctly: the entire-complete set contains the top interval [t_min(α), T(α)) and equals [1, T(α)) for α≤3/2 and for 3/2&lt;α≲1.87. Note T(α) bounds <em>entire</em>-completeness, not <em>cofinite</em>-completeness, which is larger and also non-monotone in t (at α=1.618 both conventions are cofinite at t=2.5 &gt; T). The theorem is a sufficient condition, not a characterization: it is silent
on cofinite-but-not-entire sequences and on α≥2 (where it correctly breaks down —
M→∞ as α→2). The 1-indexed "no complete point for α≥5^(1/3)" is van Doorn's
Proposition 3 (verified against the PDF in Round 3); our recurring-gap count
above is a consistency check on it, not a re-proof. An adversarial review judged
the argument sound within its stated hypotheses; its strongest noted weakness is
reach, not correctness.</p>

<p><strong>Open (updated).</strong> The closed form for t₀(α) is now in hand (errata above + the follow-up round). Still open: a Lean formalization of the sustainment lemma and the boundary; the exact 0-indexed <em>cofinite</em> frontier in t (a curve, not just spot points — and whether it yields a complete-vs-incomplete separation past t=2 anywhere in [1.71, 2): at (1.7, 2) the 0-indexed sequence shows only ~187 missing integers to 67M but a largest gap near 42M that did not stabilize, so it may be a cofinite island there or not); the t&gt;0 extension; and the full 0-indexed solved map inside [φ,2) — genuinely different from, and larger than, the one the literature has been solving.</p>

<p><strong>Round 5 — the capstone: a closed form, a cross-family proof, and a 1964 structure in disguise.</strong> The 0-indexed entirely-complete boundary has a closed form, and it is now <em>triply</em> confirmed: our exact-rational computation (the supremum to 8·10⁻²⁸ over an adversarial α-set), a same-family adversarial pass that caught the non-monotonicity, and a decorrelated GPT-5 Pro proof. The Pro argument is the cleanest of the three and worth naming: its upper bound is a three-line induction — entire-completeness forces a_n ≤ 2^n (since the partial sum C_{n-1} ≤ 2^n − 1), hence t·α^n &lt; 2^n+1 for every n, hence t ≤ min over n of (2^n+1)/α^n, with <strong>no monotonicity assumption</strong>; its lower bound is a <em>local doubling lemma</em> (⌊αx ≤ 2⌊x⌋ once ⌊x⌋ is large enough) that closes entire-completeness across the whole shelf [(2/α)^k, (2^k+1)/α^k). At the boundary t₀ the next term is 2^k+1 against the ceiling 2^k, so t₀ is a <strong>supremum, never attained</strong>. (The f(n),M sustainment lemma from Round 4 turns out to be unnecessary — the doubling closes it directly.)</p>

<p><strong>The shape of the complete set.</strong> It is not an initial interval. The shelf [(2/α)^k, (2^k+1)/α^k) is always entirely complete (proven), but for many α the entire-complete set extends below the shelf and can even be disconnected: at α=1.9 it is the single interval ≈(1.053, 1.304) (t=1 is <em>not</em> in it — the permanent gap is at 12), while at α=1.95 it is two islands, ≈(1.026, 1.029) and ≈(1.052, 1.170). All of this is machine-confirmed: the boundary prefixes [1,3], [1,2,5], [1,2,4,8,17], [1,2,4,8,16,33] with permanent gaps 2,4,16,32; the shelves proven entire; the α=1.95 island entire while the hole between the islands is not. One clean structural fact falls out of the provenance below: for t&lt;α, complete and entirely-complete <em>coincide</em> (so the cofinite-but-not-entire phenomenon — e.g. (1.618, 2.5), complete with 150 exceptions — can only occur at t≥α).</p>

<p><strong>Where it lives in the literature — the real payoff.</strong> Set u = t/α. The 0-indexed sequence at t is, term for term, the literature's sequence at u — the convention fork is just this reparametrization. So for t&lt;α (u&lt;1) we are inside the unit square of <strong>Graham, On a conjecture of Erdős in additive number theory, Acta Arithmetica 10 (1964), 63–70</strong>, which we read from the primary scan (the official ICM Acta Arithmetica image-PDF, OCR-verified): Lemma 1 (p.64) is our greedy criterion; Lemma 4 (p.65) is the doubling ⌊t·α^{n+1}⌋ ≤ 2⌊t·α^n⌋ once ⌊t·α^n⌋ &gt; (α−1)/(2−α) — i.e. the very move the Pro proof made; Theorem 5(I) (p.68) is the powers-of-two-then-overshoot obstruction, t·α^n &lt; 2^{n-1}+1 and t·α^{n+1} &gt; 2^n+1 (strict), on which our boundary lands exactly; Theorem 6 (p.69) writes the non-complete set as the union over m,n of the regions A_n^(m), B_n^(m), C_n^(m) — so the holes and fragments we found <em>are</em> Graham's regions, pulled back by u=t/α; and Theorem 3 (p.65) is the complete-iff-entirely-complete coincidence in the square (Graham gives the complete set area ≈ 0.85 of the square). For t≥α (u≥1) the classification is <strong>van Doorn 2026</strong> (arXiv:2602.23394), whose 1-indexed threshold min(2/α, 3/α², 5/α³) reindexes to our k=0,1,2 piece min(2, 3/α, 5/α²). So the set, its area, and its region structure are Graham's; the 1-indexed closed thresholds are van Doorn's.</p>

<p><strong>So what is genuinely new — honestly.</strong> Not the theorem. What is new: <strong>(i)</strong> the independent cold re-derivation — we conjectured the closed form from exact computation and proved it (re-deriving Graham's doubling along the way) before knowing Graham had it, a genuine reconstruction of a 60-year-old result from a 0-indexed, computation-first angle; <strong>(ii)</strong> the compact one-line min-formula for the boundary of Graham's set in the 0-indexed parameter — Graham gave the set as the complement of countably many regions, not as a closed form, and the explicit shelf [(2/α)^k, (2^k+1)/α^k) together with the least-minimizer convention k*(α) = max(0, ceil(log2((α−1)/(2−α)))) is, per the literature check, a unification not previously written down; <strong>(iii)</strong> naming the fragmentation as Graham's regions wearing 0-indexed clothes. That is a real clarity-and-unification contribution plus an independent derivation — creditable, and we believe a better and truer story than claiming a new theorem, which this is not.</p>

<p><strong>Honest calibration.</strong> The proof is not Lean-formalized. The primary Graham read was via OCR of an image-only scan: prose and the cited inequalities are clean; a few internal subscripts inside the Theorem 5 proof are garbled and not relied upon; the printed Theorem 5(I) condition 2 is a strict &gt; (not ≥). Van Doorn does <em>not</em> restate Graham's lemmas with matching numbering (his Lemma 1 ≈ Graham's Theorem 1; his Lemma 4 is his own generalization of the doubling), so we cite Graham as the primary source for the lemmas, not via van Doorn. Proven as corollaries: t₀(α)=2 for α≤3/2; t₀(α)→1 as α→2⁻ with the sharp asymptotic t₀(α) = 1 + ((2−α)/(2·log 2))·log(1/(2−α)) + o((2−α)·log(1/(2−α))); and t=1 is entirely complete iff α &lt; 13^(1/4) ≈ 1.899.</p>

<p><strong>Round 5, continued — the cofinite frontier, and the parked question gets a proof.</strong> A second Pro pass answered the cofinite question we'd left open, and every load-bearing claim in it machine-checks against our checker. Two indexing identities, both verified: term-for-term A⁰_{t,α} = S¹_{t/α,α} (so the 0-indexed problem is exactly van Doorn's 1-indexed problem with the horizontal parameter rescaled by α, and t₁⁽⁰⁾ = α·t₁⁽¹⁾); and at equal t, A⁰_{t,α} = {⌊t} ⊎ S¹_{t,α} (the identity behind the 4528→150 collapse).</p>

<p><strong>The 4528→150 collapse is exact lag-2 erosion, not vague density.</strong> Adding the leading term 2 turns the 1-indexed exception set G into G' = {m≥2 : m∈G and m−2∈G} ∪ {1 if 1∈G} — i.e. R' = R ∪ (2+R). We verified this as a literal set-equality (R⁰ = R | (R≪2), bit-for-bit on [0, 3M]), with |G| = 4528 and |G'| = 150. The mechanism is an exact complementary alignment: every one of the 1793 holes in the tail prefix's critical central band lies two units after an already-representable integer, so the 0-indexed prefix fills them all and Lemma 5 fires at r=25.</p>

<p><strong>The parked (1.7, 2) question is resolved — and the answer is no, it is not a cofinite island.</strong> For α≥φ the coefficient 1+α−α² in a_n+a_{n+1}−a_{n+2} ≥ tαⁿ(1+α−α²)−2 turns non-positive, so van Doorn's Lemma 2 gives s_n+s_{n+1} ≤ s_{n+2} for every n and Corollary 1 propagates any seed gap into infinitely many permanent gaps. With ⌊t⌋≥2 the integer 1 is a seed gap (every term is ≥2), so it can never heal: α≥φ and t≥2 ⇒ the 0-indexed sequence is incomplete, with no Prop 3 or 5^(1/3) needed. The "long clean top" our brute force saw at (1.7, 2) was the gap <em>between</em> two of these exponentially-sparse permanent gaps (their ratio tends to α² = 2.9241, confirmed); the formula M_k = 1+Σ_{j=1..k} a_{2j} yields 16 of them ≤50M, all verified genuinely missing, and our observed 42,597,428 is a real permanent gap from a <em>different</em> propagation chain — which only reinforces "infinitely many gaps."</p>

<p><strong>The sub-φ frontier, and how far completeness really reaches.</strong> For 1&lt;α&lt;φ the standing conjecture (van Doorn, open) is t₁(α)=∞ — the cofinite region is expected to be all t&gt;0 — so there is no known finite closed form for t₁ there. But it is far larger than t₀: translating our certified shelf gives t₁⁽⁰⁾(α) ≥ 3α for α≤1529/1000, and a concrete new verified point puts t₁⁽⁰⁾(809/500) ≥ 7281/1000 = 7.281 (Lemma-5 certificate reproduced exactly: 1-indexed prefix sum 242,912,917, s₃₆ = 150,120,200, the interval [35,440,664, 207,472,253] of length 172,031,590 &gt; s₃₆) versus t₀(809/500) = 1500/809 ≈ 1.854. Cofinite completeness moves so far beyond entire completeness because it only needs a long interval <em>somewhere</em> in the finite-prefix subset sums; once its length reaches the next term, translated copies overlap and Lemma 5 propagates it forever.</p>

<p><strong>An exact separation, necessarily below t=2.</strong> At (α,t) = (13/8, 3/2) the 0-indexed sequence is entirely complete (verified) while the 1-indexed one is incomplete: van Doorn's Proposition 4 gives the 1-indexed threshold b(α) = min(3/α², 5/α³) = 192/169 ≈ 1.136, and 3/2 &gt; b, whereas the 0-indexed reindex 12/13 &lt; b. The t=2 barrier is sharp in mechanism: the moment the leading 0-indexed term jumps from 1 to 2 it creates the seed gap 1, and above φ that gap never heals.</p>

<p><strong>The clean verified picture.</strong> Putting it together: for φ ≤ α &lt; 2 the 0-indexed complete set is <em>exactly</em> (0, t₀(α)] — entirely complete on [1, t₀], all of (0,1) complete (since 1/α lies below Graham's first wedge for these α), joined at 1, and nothing at t≥2. For 1 &lt; α &lt; φ it contains (0, t₀(α)] and is conjectured to be all of (0, ∞), with verified points far past t₀ (7.281 at α=1.618). So the convention fork's real content is now fully mapped: a closed-form boundary, a complete-set shape that collapses to a clean interval above φ, and a sub-φ region that bulges without known bound.</p>

<p><strong>Open.</strong> A Lean formalization of the doubling lemma, the boundary, and the φ-transition propagation; the sub-φ cofinite frontier t₁(α) (conjectured ∞ — no finite form known, and how far the complete set bulges past t₀ there); and, optionally, a figure overlaying Graham's set Z against our computed complete set. (The (1.7, 2) cofinite-island question is no longer open — see above: incomplete, by the propagated seed gap.)</p>
`,
    links: [
      { label: "erdosproblems.com/349", url: "https://www.erdosproblems.com/349" },
      { label: "Lean formalization (n:ℕ = 0-indexed; the convention tiebreaker)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/349.lean" },
      { label: "van Doorn, arXiv:2602.23394 (1-indexed reading)", url: "https://arxiv.org/abs/2602.23394" },
      { label: "GPT-Pro Prop-8 extension to α≤1.529 (1-indexed; chat transcript)", url: "https://chatgpt.com/s/t_6a65bc95723c8191870470c1e6dbc4c9" },
      { label: "Graham 1964, Acta Arithmetica 10", url: "https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/10/1/91827/on-a-conjecture-of-erdos-in-additive-number-theory" },
      { label: "Verification code — exact-rational checker + frontier sweep (lab.py, sweep.py)", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/349" },
      { label: "Graham 1964 — primary scan (ICM Acta Arithmetica X, OCR-verified Lemma 1/4, Thm 3/5/6)", url: "https://matwbn.icm.edu.pl/ksiazki/aa/aa10/aa1014.pdf" },
      { label: "GPT-Pro closed-form proof + novelty check (chat transcript)", url: "https://chatgpt.com/s/t_6a66b8b88dac8191b3ead50d49ff2916" },
      { label: "GPT-Pro cofinite frontier + 4528→150 erosion + post-φ obstruction (chat transcript)", url: "https://chatgpt.com/s/t_6a66e906117c8191aa37a7740e25c61a" },
    ],
  },
  {
    slug: "388-consecutive-product-equality",
    problemNum: 388,
    title: "#388: Round 3 — a written proof of the unequal-length finiteness, a subtle correction, and the uniformity step isolated as the whole problem",
    date: "2026-07-27",
    status: "in_progress",
    summary:
      "Can two disjoint blocks of consecutive integers, both length >3, " +
      "ever have equal products? 8·9·⋯·14 = 63·64·65·66 = 17,297,280 is " +
      "the only known example. Round 1 established fixed-pair finiteness. " +
      "Round 2: a real corollary narrows it further (fixed length RATIO " +
      "is also finite, so any infinite family needs infinitely many " +
      "distinct ratios), a 2024 paper's computer search conjectures this " +
      "IS the complete classification, and a search reaching 10 million " +
      "found nothing else across 1.4 billion comparisons. Round 3: a " +
      "follow-up wrote out the actual proof of the fixed-unequal-length " +
      "finiteness Round 2 had only cited — a clean Kulkarni–Sury " +
      "case-elimination we verified by exact computation — and caught a " +
      "subtle error in the naive root-comparison argument. It proves no " +
      "uniform bound, so the full problem stays open; everything below " +
      "the uniformity step is now settled.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/388">erdosproblems.com/388</a>,
OPEN, 0 claimed proofs). Can one classify all solutions of
∏(m1+i) for i=1..k1 = ∏(m2+j) for j=1..k2, where k1,k2 &gt; 3 and the two
blocks of consecutive integers are disjoint? Are there only finitely
many solutions?</p>

<p><strong>The one known example.</strong>
8·9·10·11·12·13·14 = 63·64·65·66 = 17,297,280 — a length-7 block equaling
a length-4 block. This is real, already in OEIS
(<a href="https://oeis.org/A163263">A163263</a>, "numbers having multiple
representations as the product of non-overlapping ranges of consecutive
numbers"), and per that sequence's own comments, a search of the gaps
between the first 45,000 primes turned up nothing further. We
re-verified the arithmetic directly: both products are exactly
17,297,280.</p>

<p><strong>Two real structural facts, one of them completely elementary.</strong>
Equal-length blocks (k1=k2=k&gt;3) can <em>never</em> collide — the product
function f_k(x)=x(x+1)⋯(x+k−1) is strictly increasing, and disjointness
forces the right block's every factor above the left block's every
factor, so f_k(m2+1) &gt; f_k(m1+1) always. Clean, self-contained, no
citation needed. For any <em>fixed</em> pair of unequal lengths (both
≥4), only finitely many solutions can exist — this leans on real
literature (Bilu–Tichy 2000; Beukers–Shorey–Tijdeman 1999; Kulkarni–Sury,
Indagationes Mathematicae 2003, specifically about x(x+1)⋯(x+m−1)=g(y))
showing the "rising factorial" polynomials here don't fall into any of
Bilu–Tichy's exceptional cases — all three citations checked real and
genuinely on-topic, not just topically adjacent.</p>

<p><strong>We didn't trust the stated search — we ran a stronger one
ourselves.</strong> Independently reproduced the claimed computational
search (lengths up to 15, starting point up to 5,000) using an exact
integer-root method rather than floating-point approximation, then
extended it well past the original scope: lengths up to 35 with starting
points up to 30,000 (14.88 million triples, fully complete), and lengths
up to 15 with starting points up to 1,000,000 (partially complete at
report time). Nothing beyond the one known solution turned up anywhere.</p>

<p><strong>Round 1's open question, and what Round 2 pushed on.</strong>
The general question — allowing BOTH lengths to vary, not just fixed
pairs — had no proof of finiteness; only a structural reason to expect
one (the shorter block must be smooth relative to the taller block's
endpoint, genuinely rare by size, but not yet a sufficient bound). We
sent a follow-up asking a second model to narrow that gap directly.</p>

<p><strong>A real new corollary: fixed RATIO is also finite, not just
fixed pair.</strong> Beukers–Shorey–Tijdeman's 1999 theorem gives
finiteness for every fixed pair of lengths (k₁,k₂) — Round 1's result.
Combining it with Saradha–Shorey–Tijdeman's 1995 theorem (Math. Proc.
Cambridge Philos. Soc. 117, confirmed real) — which effectively bounds
solutions whenever the length ratio k₁/k₂ is fixed AND gcd(k₁,k₂)&gt;1 —
gives something stronger: fixed length ratio k₁/k₂, in lowest terms,
is <em>also</em> only finitely many solutions (the gcd&gt;1 multiples are
covered by Saradha–Shorey–Tijdeman directly; the remaining coprime pair
itself is covered by Beukers–Shorey–Tijdeman). The real consequence:
any hypothetical infinite family of solutions can't sit on a single
ray like (k₁,k₂)=(7t,4t) for varying t — or on any finite collection of
such rays. It would have to use infinitely many genuinely distinct
reduced ratios. That's new, checked against both cited papers directly
(both real, on-topic, confirmed independently — not just accepted).</p>

<p><strong>A 2024 paper's computer search suggests — doesn't prove —
that the known solution is the ONLY one.</strong> Wataru Takeda's 2024
paper (Bull. Iranian Math. Soc. 50, Paper No. 64 — real, confirmed)
studies the more general equation ℓ₁!ℓ₂!=k₁!k₂! and computationally
suggests exactly three nontrivial solution tuples exist in total,
across all factorial-argument sizes: (7,13;4,15) — i.e. 5·6·7=14·15 —
(14,62;7,66) — our known #388 solution — and (22,54;18,57) — i.e.
19·20·21·22=55·56·57. We re-verified all three products by hand; all
exact. Only the middle one has both block lengths ≥4, which is exactly
#388's own requirement — so Takeda's list, if it really is complete,
says (7,7,62,4) is the ONLY answer to #388. But "computationally
suggests" is doing real work in that sentence: Takeda's own paper does
not claim this as a theorem, and neither do we.</p>

<p><strong>A genuinely new, verified structural tool: multiplicative
valuation transport.</strong> Any solution can be written as a set of
"packages" — for every lower-block term and upper-block term that
share a prime factor, the shared prime-power must divide the
difference between those two specific terms. This falls out of a
completely elementary transportation-matrix argument (given two
sequences of nonnegative integers with equal sums, a matrix with those
row/column sums always exists) — we re-derived it independently and it
holds. Applied to the known solution, it gives an exact, checkable
"transport certificate": 63=9×7, 64=8×2×4, 65=5×13, 66=11×3×2, and
running it backward recovers every original term (10=2×5, 12=4×3,
14=7×2, etc.) — we verified every cell of this table by hand. It also
proves cleanly that any prime larger than the longer block length must
transport along exactly one edge — useful structure, but explicitly
not yet a finiteness proof; the response is honest that this "exposes
the obstruction cleanly" without closing it.</p>

<p><strong>The search got deeper, and stayed clean.</strong> An
independent exact-integer search (GMP arbitrary precision, no floating
point) covered every solution with lengths 4–20 and every term up to
10,000,000 (1.42 billion comparisons) and lengths 4–100 up to 100,000 —
both complete, both turning up nothing but the one known solution. A
separate Erdős–Selfridge tie-in is correctly ruled out as inapplicable
(that theorem is about a single product never being a perfect power;
our equation is two different factorizations of the same number, which
isn't a perfect power here — 2⁷3³·5·7·11·13 — so it's philosophically
adjacent, not a real tool). A February 2026 preprint by Saša Novaković
(arXiv:2602.23838, confirmed directly against its own abstract) proves
a related abc-conjecture-conditional finiteness result for factorial
products, but explicitly for the asymmetric case (different numbers of
factorial factors on each side) — correctly noted as not covering
#388's balanced two-versus-two case.</p>

<p><strong>Round 3: the fixed-unequal-length finiteness now has a written
proof, not just a citation.</strong> Round 2 asserted — correctly, by
citation — that for any fixed unequal pair of lengths (both ≥4) only
finitely many solutions exist, leaning on Kulkarni–Sury 2003 and
Beukers–Shorey–Tijdeman 1999. A follow-up went and wrote the proof out.
Write F_k(X)=X(X+1)⋯(X+k−1); a block product is F_k(m+1). Kulkarni–Sury's
Theorem 1.1 (a consequence of the Bilu–Tichy classification of polynomial
Diophantine equations) says that if F_M(x)=g(y) has infinitely many
rational solutions with bounded denominator, then g must take one of three
shapes. Put the longer factorial on the F_M side (M&gt;N≥4) and all three
die: the first would force N=M·deg(h)≥M, contradicting N&lt;M; the third
exists only for M=4, impossible since M≥5; the second requires M even with
F_N=Φ_M∘h, where Φ_M(T)=∏(T−(2j−1)²/4). That last one is the content, and
it falls to a root-geometry argument: degree-counting gives M=2N and h
linear with leading coefficient ±1, so h would carry the roots of F_N —
the arithmetic progression 0,−1,…,−(N−1), diameter N−1 — bijectively onto
the roots of Φ_{2N}, the odd squares over four, diameter N(N−1). Equal
sets would force N−1=N(N−1), i.e. N=1, absurd for N≥4.</p>

<p><strong>We verified the load-bearing mathematics ourselves.</strong>
The whole argument rests on the centered-square decomposition
F_{2q}(X)=Φ_{2q}((X+(2q−1)/2)²) — the structural fact that makes the
second exceptional shape take exactly the Φ_M form. We checked it
symbolically for q=2,3,4,5 (it holds), independently confirmed the
odd-square root set and the diameter collision N−1≠N(N−1) for several N,
and re-confirmed the known solution F_7(8)=F_4(63)=17,297,280 sits outside
every exceptional pattern (its (7,4) pair is not the M=2N degree shape),
exactly as an isolated point should. The one thing taken on trust is the
literal statement of Kulkarni–Sury's theorem — a real paper (the DOI
resolves), already vetted in Round 2, whose three-case shape is exactly
what the verified decomposition generates — rather than a fresh reading of
the source PDF.</p>

<p><strong>A subtle correction worth keeping.</strong> The tempting
one-line move — "just compare the arithmetic-progression roots of the two
sides" — is only valid in that second (Φ_M∘h) branch, where Kulkarni–Sury
normalize the shape precisely. In the outer-linear branch the Bilu–Tichy
theorem allows an output translation, so the zero set of F_M is not
itself fixed; there the correct obstruction is the multiplicity structure
of arbitrary shifted fibers F_M−c, not the root positions. Anyone writing
this up needs the distinction; the naive version would be wrong.</p>

<p><strong>What's still open — now more isolated than ever.</strong>
Round 3 proves the unequal-length finiteness for real; Round 2 had the
fixed-ratio corollary; equal lengths never collide at all. So every regime
below the full question is settled. What remains is exactly the uniformity
step Round 1 named: none of these finiteness results gives a bound that
survives as both lengths grow while the ratio between them ranges over
infinitely many values. An infinite family is not ruled out — it would
just have to use infinitely many distinct reduced ratios, growing without
bound, which the smoothness heuristic says is implausible but nothing yet
proves impossible. Takeda's verified-arithmetic conjecture (the known
(7,7,62,4) solution is the only one) remains the credible picture of the
full answer, not a proof. Genuinely open.</p>
`,
    links: [
      { label: "GPT-Pro Round 3 — the written unequal-length finiteness proof + correction (chat transcript)", url: "https://chatgpt.com/s/t_6a66d4db3f2481919ea3e90020721abc" },
      { label: "GPT-Pro Round 2 — fixed-ratio corollary + 1.4B-comparison search (chat transcript)", url: "https://chatgpt.com/s/t_6a65b0e6d9a48191ae77cdee58368850" },
      { label: "erdosproblems.com/388", url: "https://www.erdosproblems.com/388" },
      { label: "OEIS A163263", url: "https://oeis.org/A163263" },
      { label: "Kulkarni–Sury, Indag. Math. 14 (2003)", url: "https://doi.org/10.1016/s0019-3577(03)90069-3" },
      { label: "Novaković, arXiv:2602.23838 (Feb 2026)", url: "https://arxiv.org/abs/2602.23838" },
    ],
  },
  {
    slug: "614-induced-min-degree-turan",
    problemNum: 614,
    title: "#614: Round 3 — the near-diagonal regime (ERSS 1996 + Pikhurko–Thomason 2002), and an unconditional floor under the fixed-k story",
    date: "2026-07-27",
    status: "in_progress",
    summary:
      "f(n,k) is the fewest edges forcing every (k+2)-set of vertices to " +
      "induce a subgraph with a vertex of degree ≥k. Round 1 reduced it " +
      "to a finite-family Turán problem and flagged the general formula " +
      "as unproven. Round 2 pushed on that gap — and mostly settled it, " +
      "except for one claim we caught overreaching: it silently treated " +
      "the 50-year-open Erdős–Simonovits even-cycle conjecture as solved. " +
      "Corrected, and the corrected version is the more interesting " +
      "finding: for most k, a clean formula is provably at least as hard " +
      "as that named open problem — that's WHY it doesn't exist, not " +
      "just that nobody's found it yet. Round 3 maps the regime Round 2 " +
      "left untouched — the near-diagonal one (n−k small): the actual " +
      "1996 Erdős–Reid–Schelp–Staton theorem and Pikhurko–Thomason's 2002 " +
      "follow-up, which disproves the ERSS conjecture, gives the k→∞ " +
      "asymptotic, and proves the naive split-graph fails off-diagonal — " +
      "plus an unconditional f(n,k)=C(n,2)−o(n²) for every fixed k. The " +
      "fixed-k orders Round 2 already proved (k=2,3,…) re-derive here; " +
      "they're confirmation, not new ground.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/614">erdosproblems.com/614</a>,
[FRS97] — Faudree, Rousseau, Schelp, "Problems in graph theory from
Memphis," 1997 — which just poses the question, no bounds). f(n,k) is
the minimal number of edges in a graph on n vertices such that every
set of k+2 vertices induces a subgraph with a vertex of degree at
least k. Determine f(n,k).</p>

<p><strong>A real, easy-to-miss source: a single forum comment, one
attached PDF, three weeks before we looked.</strong> The problem's own
page has no recorded progress — but its discussion thread has exactly
one comment, posted by Quanyu Tang on 7 Jan 2026: "Ma and I wrote a
short note on this problem, showing that it can be reformulated as a
finite-family Turán problem," with a link to a real GitHub PDF. We
fetched and read the actual 6-page note directly (not just the comment
summary) — Theorem 2.1, 3.1 (proved via Dirac's theorem), the general
reduction (Lemma 4.2/4.3, Theorem 4.5), explicit forbidden families
computed up to k=6 by exhaustive Mathematica search. Everything checked
against the primary source, not the paraphrase.</p>

<p><strong>The reduction, and why it's actually a clean trick.</strong>
In the complement graph H, "some vertex has degree ≥k inside the
(k+2)-window" becomes "some vertex has degree ≤1 inside the window" —
so the whole condition becomes "H contains no INDUCED copy, on any
k+2 vertices, of a minimum-degree-≥2 graph." Because the forbidden
graphs have exactly k+2 vertices (matching the window size exactly),
avoiding induced copies turns out to be equivalent to avoiding ordinary
(non-induced) copies of just the EDGE-MINIMAL such graphs — a classical
Turán number. Explicit families: k=1 → {K₃} (Mantel's theorem exactly);
k=2 → {C₄} (the classical Kővári–Sós–Turán quantity, ~n^(3/2)/2, no
simple closed form); k=3 → three graphs (a 5-cycle, K₂,₃, and a
"bowtie" — two triangles sharing a vertex).</p>

<p><strong>Independently verified three separate ways, not just
re-read.</strong> (1) Worked through the induced-vs-non-induced
equivalence by hand before even reading the Tang/Ma note — it's a
legitimate, non-circular edge-deletion argument. (2) Brute-force
enumerated every graph on 3, 4, and 5 vertices to independently confirm
the k=1,2,3 forbidden families match exactly. (3) Used an independent
constraint solver (Google OR-Tools CP-SAT, not their method) to compute
14 small exact values of f(n,k) directly from the original definition —
all 14 matched the note's claims exactly — then went further and
cross-checked the REDUCTION itself end-to-end: computed the Turán
numbers via a separately-encoded model and confirmed
C(n,2)−ex(n,F) = f(n,k) independently for 8 more cases, including a new
value (ex(8,C₄)=11) that correctly matches the known OEIS record for
that quantity.</p>

<p><strong>One real correction, one honest flag.</strong> The forum
comment credits "Ma and I" — two people, Quanyu Tang and a coauthor
Ma, confirmed via a real, separately-published paper by the same pair
on a different Erdős problem. An earlier draft here mis-transcribed
this as a single hyphenated name; fixed. Separately: the general
asymptotic f(n,k) = C(n,2) − Θ(n^(2−1/r)) for large k is plausible
(every forbidden family checked so far contains a bipartite member,
which is what drives the Kővári–Sós–Turán upper bound) but is NOT
actually proven in the Tang/Ma note, which only gives explicit families
up to k=6 — flagging it here as a reasonable extrapolation, not an
established fact.</p>

<p><strong>Round 1's honest flag, and what Round 2 asked.</strong> No
simpler closed form than "Turán number of an explicit finite family"
was known for general k, and the natural guess — f(n,k) =
C(n,2)−Θ(n^(2−1/r)) for some r(k), driven by a bipartite member of the
forbidden family — was flagged explicitly as an unproven extrapolation.
We sent a follow-up brief asking a second model to settle it: does
every forbidden family F_k^min contain a bipartite member, and if so,
does the matching upper AND lower bound actually go through?</p>

<p><strong>Round 2: real progress on part of it, a real overclaim on
the rest.</strong> The genuinely solid part: for every k≥2, K_{2,k}
(the complete bipartite graph with parts of size 2 and k) belongs to
F_k^min — clean, checkable (every edge touches a degree-2 vertex, so
deleting any edge breaks minimum-degree-2) — and whenever the family's
sparsest bipartite member turns out to be C₄-containing (which includes
every case checked through k=7 except the pure-even-cycle cases below),
a bipartite C₄-free construction avoids the whole family at once
(non-bipartite members like C₅ or the "bowtie" are avoided for free,
since bipartite graphs have no odd cycles). That genuinely nails down
f(n,k) = C(n,2) − Θ(n^(3/2)) for k=1,3,5 and, since C₄=K_{2,2} directly,
k=2 as well — real, checkable, correct.</p>

<p><strong>The overclaim: for even-cycle-driven k, "the order is again
tight" is not established — it's the Erdős–Simonovits conjecture.</strong>
When k is even, C_{k+2} (a pure cycle) sits in F_k^min too, giving a
proven Bondy–Simonovits UPPER bound O(n^{1+2/(k+2)}). The response then
claimed a matching lower bound exists in general via "standard
existence results for high-girth graphs," concluding the order is
"again tight" for every even k. We checked this specific claim against
the literature directly: matching lower bounds for even-cycle Turán
numbers are known ONLY for cycle lengths 4, 6, and 10 (via generalized
quadrangle/hexagon incidence-graph constructions) — every other even
cycle length is the Erdős–Simonovits conjecture, open since the 1980s,
with no progress on the general case as of 2025. Concretely: k=4 (C₆)
is fine, genuinely resolved (Θ(n^{4/3})) — but k=6 (C₈), the very next
even case in the response's own worked table, is NOT resolved by
anything in the literature. The response's "again tight" line quietly
assumed a 50-year-open conjecture as a routine corollary.</p>

<p><strong>The corrected conjecture, and two exact orders that fall
out for free.</strong> Reframing around the right parameter cleans the
whole picture up. Put m=k+2 and set s_k=(k+2)/2 for even k and
s_k=⌊(k+3)/3⌋ for odd k — half the largest girth a bipartite member of
F_k^min can have. (When k is even that member is the pure cycle C_{k+2};
when k is odd it's a balanced generalized theta graph Θ_{2a,2b,2c},
where bipartiteness forces a degree-3 branch vertex and spends vertices
less efficiently — a parity sawtooth, not a smooth formula.) The
natural corrected form is then f(n,k)=C(n,2)−Θ_k(n^{1+1/s_k}), and the
proposed integer-r shape n^{2−1/r} is simply wrong: 1+1/s=2−1/r has an
integer solution r≥2 only at s=2. The upper bound is Bondy–Simonovits
(even k) or Liu–Yang's same-parity theta-graph theorem (odd k); the
matching lower bound is a high-girth construction that avoids the WHOLE
family at once — any bipartite graph of girth &gt; 2s_k is automatically
F_k^min-free, since every bipartite member has girth at most 2s_k. That
lower bound is exactly the classical even-cycle problem, so the
corrected conjecture is proved unconditionally precisely where matching
high-girth graphs are known: s_k∈{2,3,5}, i.e. k∈{2,3,4,5,7,8,13}
(plus k=1 by Mantel). Two of those are apparently-new exact orders the
reduction yields for free: <strong>f(n,7)=C(n,2)−Θ(n^{4/3})</strong>
(upper member Θ_{2,4,4}, lower a generalized-quadrangle incidence graph,
girth 8) and <strong>f(n,8)=C(n,2)−Θ(n^{6/5})</strong> (upper member
C₁₀, lower a generalized-hexagon incidence graph, girth 12).</p>

<p><strong>Round 3: the near-diagonal regime Round 2 never touched.</strong>
Rounds 1–2 worked in the fixed-k, n→∞ regime. There's a complementary one:
n−k small (k close to n). A fresh reasoner run dug out the actual literature
there, and it's worth recording even though it doesn't move the fixed-k
frontier. The problem is the j=2 case of a function q(a;j;ℓ) — the minimum
number of edges on a+j+ℓ vertices forcing every a+j of them to induce maximum
degree at least a — so f(n,k)=q(k;2;n−k−2). Erdős, Reid, Schelp and Staton
(Discrete Mathematics 158, 1996) proved the exact formula
q(a;j;ℓ)=(ℓ+1)a+C(ℓ+1,2) whenever a≥max{jℓ, C(ℓ+2,2)}: the split-graph
G₀=(K_t∨K̄_k)∪K₁ (which we verified is admissible) is exactly optimal deep in
the near-diagonal — and they conjectured it throughout the much wider range
a≥j+ℓ.</p>

<p><strong>Pikhurko–Thomason 2002 disproves that conjecture, and pins down
more.</strong> Their "Disjoint subgraphs of large maximum degree" (Discrete
Mathematics 248, 2002, 125–141; we confirmed the citation is real) shows the
ERSS conjecture is FALSE: the split-graph value fails whenever a&lt;(j−1)ℓ,
which for us is n&gt;2k+2 — so G₀ is provably NOT globally optimal, exactly the
off-diagonal direction our fixed-k theory also points. They prove the
asymptotic q=(1+o(1))(ℓ+1)a(1+ℓ/(2a+2j)) as a→∞ with ℓ=o(a(a+j)/log(a+j)) —
note this is a k→∞ statement, NOT a fixed-k one — and extend the exact q=F₀
range to a≥(j+½)ℓ+(2j+ℓ)/(4j−2), i.e. 11k≥8n−14 for us. We found no post-2002
improvement (a search report, not a guarantee).</p>

<p><strong>An unconditional floor under the whole fixed-k story.</strong> A
clean complement codegree bound — if two vertices of the complement H share k
neighbors, those k+2 vertices already have minimum degree ≥2 (forbidden), so
every pair shares at most k−1; double-count cherries and use convexity — gives
f(n,k)≥C(n,2)−(n/4)(1+√(1+4(k−1)(n−1)))=C(n,2)−(√(k−1)/2)n^{3/2}−O_k(n), and a
high-girth bipartite complement gives f(n,k)≤C(n,2)−Ω_k(n^{1+1/(L−1)}). Hence
f(n,k)=C(n,2)−o(n²) for every fixed k≥2, unconditionally — a floor that holds
even where the exact order (Round 2's s_k conjecture) is still the
Erdős–Simonovits wall. The run also re-proved the f(n,2)=f(n,3)=C(n,2)−Θ(n^{3/2})
matching order and re-derived the k=1,2,3 forbidden families (with the exact
labeling counts 12 C₅ / 10 K₂,₃ / 15 bowtie) — all of which Round 2 already
had, so we record them as confirmation, not new ground. We verified the
load-bearing pieces on our side: the codegree algebra, the F₃^min
classification and counts, ex(5,F₅)=7, the split-graph admissibility, the
projective-plane lower bound for k=3, and the Pikhurko–Thomason citation.</p>

<p><strong>Where Round 3 leaves it.</strong> The near-diagonal regime is now
mapped (ERSS exact where k is a large fraction of n; Pikhurko–Thomason's
asymptotic as k→∞; the split-graph provably failing past n&gt;2k+2). The fixed-k
regime is pinned for k∈{1,2,3,4,5,7,8,13} (Round 2). The frontier is unchanged
and named: the very next case, k=6 (s₆=4, C₈ in the family), needs a matching
Ω(n^{5/4}) construction for the whole family — which would in particular settle
the open C₈ Turán order — and every k with s_k∉{2,3,5} meets the same
Erdős–Simonovits wall. The two regimes are consistent (the near-diagonal exact
formula and the fixed-k Θ(n^{1+1/s_k}) order are different limits of the same
quantity) but nobody has bridged them — and the general problem remains at
least as hard as a named, famous, genuinely unresolved one.</p>
`,
    links: [
      { label: "GPT-5.6 Sol Round 3 — near-diagonal regime (ERSS/Pikhurko–Thomason) + unconditional floor (chat transcript)", url: "https://chatgpt.com/s/t_6a66debbedb88191a3eb9b5d5950ce6c" },
      { label: "Pikhurko–Thomason, Discrete Math. 248 (2002), 125–141", url: "https://doi.org/10.1016/S0012-365X(01)00190-X" },
      { label: "erdosproblems.com/614", url: "https://www.erdosproblems.com/614" },
      { label: "erdosproblems.com/614 forum thread", url: "https://www.erdosproblems.com/forum/thread/614" },
      { label: "Tang & Ma's note (GitHub PDF)", url: "https://github.com/QuanyuTang/erdos-614-turan-reduction/blob/main/erdos614_note.pdf" },
      { label: "Erdős–Simonovits even-cycle conjecture (erdosproblems.com)", url: "https://mathweb.ucsd.edu/~erdosproblems/erdos/newproblems/TuranEvenCycleLowerBound.html" },
      { label: "Liu & Yang, On the Turán Number of Generalized Theta Graphs (arXiv:2103.10200)", url: "https://arxiv.org/abs/2103.10200" },
      { label: "GPT-5.6 Sol Round 2 — corrected s_k asymptotic + k=7,8 exact orders (chat transcript)", url: "https://chatgpt.com/s/t_6a66cc4cac088191b414c45ac25546a6" },
    ],
  },
  {
    slug: "452-omega-loglog-run",
    problemNum: 452,
    title: "#452: Round 2 — the \"no upper bound exists\" line from yesterday is now wrong",
    date: "2026-07-26",
    status: "in_progress",
    summary:
      "How long a run of consecutive integers can stay above the normal " +
      "prime-factor count ω(n) > log log n? Round 1 gave the explicit CRT " +
      "lower-bound construction and reported the honest bad news: no " +
      "non-trivial upper bound existed anywhere. Round 2, same day: a " +
      "second model built a real one — a genuine sieve-theoretic upper " +
      "bound miles below the trivial prime-gap bound, with a fully " +
      "checkable 5-integer example. Half its six background literature " +
      "citations didn't survive verification and are dropped below; the " +
      "actual proof — checked independently, not just accepted — " +
      "doesn't depend on any of them.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/452">erdosproblems.com/452</a>,
OPEN, 0 claimed proofs). Let ω(n) count the distinct prime factors of n.
What is the size of the largest interval I ⊆ [x,2x] with ω(n) &gt; log log n
for every n in I? Write L(x) for that largest length.</p>

<p><strong>Round 1 recap.</strong> The erdosproblems.com page states,
as a bare fact with no construction: Erdős [Er37] proved
{n : ω(n) &gt; log log n} has density 1/2, and "the Chinese remainder
theorem implies" a lower bound of (1+o(1))·log x/(log log x)². We built
the actual explicit CRT construction behind that sentence (fix
k=⌊log log x⌋+2, take the first m≈(1−ε)log x/log log x primes in
disjoint blocks of size k, one CRT system forces k prime divisors onto
every offset in the run) and reported, honestly, that no non-trivial
upper bound existed anywhere — only the trivial O(x^0.525) largest-prime-gap
bound (Baker–Harman–Pintz).</p>

<p><strong>Round 2: that "no upper bound" line is now wrong.</strong>
A second model (GPT-5.6 Sol, independent run) built a real one — not
matching the lower bound, but a genuine, non-trivial, sieve-derived
upper bound sitting far below the trivial prime-gap bound:</p>

<p style="text-align:center">(1−o(1))·log x/(log log x)² ≤ L(x) ≤ exp((1+o(1))·log x/log log x)</p>

<p>We checked the ordering ourselves numerically: at x=10²⁰ the new
upper bound (≈4.3×10⁸) is already far below the trivial prime-gap bound
(≈3.2×10¹⁰) and comfortably above the CRT lower bound (≈3.1) — no
contradiction, and the gap between the two sides, while still real, has
shrunk from "polynomial in x" to "x^(o(1))". The mechanism: a
Richert-type weighted sieve (weight w(n) = η − Σ a_p over primes p in a
window [z,y), tuned so the total weight W = H·V(z)·(1+o(1)) is
positive) proves any interval of length H ≥ exp((1+o(1))·log x/log log x)
must contain a point with ω(n) below the log log n threshold —
contradicting the defining property of an admissible run. This is
standard weighted-sieve machinery (the model's own label, not ours —
it explicitly declined to claim novelty), but we didn't find it stated
anywhere on the problem page or elsewhere, so it's new information for
the tracker even if not new to sieve theory.</p>

<p><strong>What we independently verified, not just accepted.</strong>
(1) The explicit 5-integer certificate — n=1,749,715,245,053,405,893,340
with n,…,n+4 forced to carry ω=(7,6,5,6,5) distinct prime factors via a
specific small-prime assignment — we refactored all five numbers from
scratch in Python; every factorization matches exactly, and
log log(n+4)=3.8901&lt;4≤ω(n+i) for all five, confirmed. (2) The
"forced-incidence barrier" — a clean argument bounding why any purely
CRT-forced certificate (the Round 1 style of construction) can't beat
H≤(1+o(1))·log x/(log log x)² no matter how cleverly primes are reused
— we rederived the Mertens-sum step (Σ_{p≤H} 1/p ~ log log H) and the
large-prime pigeonhole step by hand; it's correct. (3) The final
asymptotic simplification from the exact intermediate bound to the
clean exp((1+o(1))·log x/log log x) form — checked numerically, ratio
of exponents converges toward 1 as claimed.</p>

<p><strong>The literature audit around the proof was worse than the
proof itself — worth naming plainly.</strong> The response cited six
background papers to frame "what's already known nearby." We
independently verified all six, and only half hold up. Real and
accurate: Erdős–Pomerance–Sárközy's "On Locally Repeated Values of
Certain Arithmetic Functions, IV" (Ramanujan J. 1, 1997 — the response
paraphrased the title but the content match is exact, confirmed
against the actual abstract), Matomäki's "Almost Primes in Almost All
Very Short Intervals" (confirmed, Richert-weighted-sieve mechanism
matches), and Iwaniec's 1978 "On the Problem of Jacobsthal"
(Demonstratio Math. 11, confirmed). Three did not survive: a claimed
"Erdős–Kátai 1979" paper defining local-extrema quantities
O_k(n)/o_k(n) — we found the real 1979 Acta Math. Hungar. 33 paper at
that citation, and it exists, but it's solo-authored by Erdős
("Some Unconventional Problems in Number Theory"), has nothing to do
with Kátai, and contains no O_k/o_k content anywhere in its ten pages
— a real citation wearing the wrong content; an "Erdős–Sárközy 1994"
paper on "consecutive large values"; and a "2017 Tao MathOverflow
comment." Neither of the last two turned up anywhere despite both
areas being well-indexed — genuinely unable to confirm they exist. All
three are dropped from what we're citing below. None of this touches
the actual sieve proof, the forced-incidence-barrier argument, or the
numeric certificate — all three were checked directly, not via
citation — but it's a real reminder that a model's supporting
literature texture can fail even when its core mathematics holds, and
the two failure modes don't announce themselves differently.</p>

<p><strong>What's still open.</strong> The gap between the two sides is
still real — a CRT-scale lower bound versus an x^(o(1))-scale upper
bound — just categorically smaller than "polynomial vs. exponential."
An Erdős–Kac heuristic (treating "ω(n) above normal order" as roughly
i.i.d. Bernoulli(1/2)) predicts the true answer sits at L(x) ≍ log x,
well below even this improved upper bound. Closing that remaining gap
in either direction is genuinely open.</p>
`,
    links: [
      { label: "erdosproblems.com/452", url: "https://www.erdosproblems.com/452" },
      { label: "Baker–Harman–Pintz prime gaps", url: "https://en.wikipedia.org/wiki/Prime_gap#Numerical_results" },
      { label: "Matomäki, almost primes in almost all very short intervals", url: "https://arxiv.org/abs/2012.11565" },
      { label: "Iwaniec, on the problem of Jacobsthal (1978)", url: "https://www.degruyter.com/document/doi/10.1515/dema-1978-0121/html" },
      { label: "GPT-5.6 Sol Round 2 — the sieve upper bound + CRT certificate (chat transcript)", url: "https://chatgpt.com/s/t_6a65a70dca108191967e56267390d36c" },
    ],
  },
  {
    slug: "142-white-whale",
    problemNum: 142,
    title: "#142: our white whale — we didn't land it, but here's the real, current state of the hunt",
    date: "2026-07-26",
    status: "declined",
    summary:
      "Erdős's largest bounty ($10,000): an actual asymptotic formula for " +
      "r_k(N), the size of the largest subset of {1,...,N} with no " +
      "non-trivial k-term arithmetic progression. \"Probably " +
      "unattackable,\" Erdős said — and it still is. We sent two " +
      "frontier models after it independently, expecting no proof, and " +
      "got no proof — but both surfaced and verified two genuine 2024–" +
      "2026 breakthroughs most casual summaries (including our own " +
      "brief) had gotten stale, plus a precise account of exactly why " +
      "\"formula\" is a different kind of hard than \"bounds.\"",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/142">erdosproblems.com/142</a>,
$10,000 — Erdős's largest offer). r_k(N) is the largest subset of
{1,...,N} with no non-trivial k-term arithmetic progression. Not "find
matching bounds" — an actual asymptotic <em>formula</em>. Erdős called
it "probably unattackable at present." We went after it anyway on
purpose (Patrick's framing: "it can be our white whale") — cheap to
ask, essentially certain to fail, worth it for what a real attempt
would surface. We ran it through Codex, then separately through Opus 5
and Fable 5, independently, no cross-talk. All three: HONEST DECLINE.
Exactly as expected. What's actually interesting is what came back
with the decline.</p>

<p><strong>The literature has moved twice since anyone last summarized
it casually, and both models found it, independently, and we verified
both citations are real.</strong> (1) Behrend's 1946 lower-bound
constant — unbeaten for 78 years — was improved for the first time in
June 2024: Elsholtz, Hunter, Proske, and Sauermann
(<a href="https://arxiv.org/abs/2406.12290">arXiv:2406.12290</a>)
give the first quasipolynomial improvement, moving the constant from
Behrend's 2√2≈2.828 to about 2.667 (in the standard normalization),
plus a companion finite-field result breaking the classical c=1/2
barrier. (2) On the upper-bound side, a March 2026 preprint by
Raghavan pushes the known exponent past Bloom–Sisask's announced-but-
undetailed 5/41 to 1/6 (up to a log-log factor) — originally confirmed
only indirectly, via Wikipedia's Roth's-theorem article citing it. Two
further independent runs (Grok, no cross-talk with the first two)
landed on the exact same two citations and gave us the precise primary
source we were missing: <a href="https://arxiv.org/abs/2603.27045">arXiv:2603.27045</a>,
"Improved Bounds for 3-Progressions," March 2026, revised May 2026 —
now confirmed directly, not just by inference. Four models, zero
cross-talk, identical literature map. Both findings real, both recent,
both things a casual "state of the art" summary (including our own
original brief, which we now know was already stale) would have
missed.</p>

<p><strong>The actual reason a formula is categorically harder than
matching bounds, stated precisely by both models converging on the
same structure independently.</strong> Write the "deficiency"
F(N)=log(N/r_3(N)). A formula needs, in order: that F(N) has a single
well-defined shape (log N)^θ (not proven — even θ's <em>existence</em>
is open); a specific constant at that scale (moved in 2024, so nobody
has a candidate); the sub-leading correction (moved in 2010); and the
whole thing matching to 1+o(1). One model (Opus 5) proved directly that
the standard tool for guaranteeing such a constant exists at all
(Fekete's subadditivity lemma) is <em>provably useless</em> at the
actual scale √(log N) the problem lives at — meaning it's not just
unproven what the constant is, it's unproven that the constant a
formula would have to name even exists. The other (Fable 5)
independently derived essentially the same obstruction from a
different angle (a near-subadditivity argument) and framed it as two
genuinely separate open problems bundled inside one: does the shape
exist, and only then, what is it. Both flagged the same historical
cautionary tale — Szekeres's 1936 conjectured formula for this exact
problem was disproven six years later, and nobody has proposed a
candidate formula in print since.</p>

<p><strong>Real side mathematics, clearly labeled as not progress on
#142 itself.</strong> Both models independently found and proved an
exact formula for r_k(N) in the opposite regime — N bounded in terms of
k, not k fixed and N→∞ — and both, independently, discovered it
fractures almost immediately into arithmetic (mod-2, mod-6, ...)
casework rather than staying a smooth function. Neither claims this as
progress; both flag it as a small, honest, verified side-result and a
cautionary data point (if the one regime where an exact answer exists
looks arithmetically messy rather than clean, that's mild evidence
against expecting a clean formula anywhere).</p>

<p><strong>Why we're shipping a decline.</strong> Same standing policy
as #389's "we got refuted and found something real anyway" — a real,
well-verified negative result and an accurate, current map of a hard
problem is a legitimate outcome, not a consolation prize. Erdős's
"probably unattackable at present" remains, as both models put it,
exactly right — and now we know precisely how right, with the map
freshly redrawn.</p>
`,
    links: [
      { label: "erdosproblems.com/142", url: "https://www.erdosproblems.com/142" },
      { label: "Elsholtz–Hunter–Proske–Sauermann, arXiv:2406.12290", url: "https://arxiv.org/abs/2406.12290" },
      { label: "Raghavan, arXiv:2603.27045", url: "https://arxiv.org/abs/2603.27045" },
    ],
  },
  {
    slug: "489-394-starfleet-independent-verification",
    problemNum: 489,
    title: "independently rebuilding Colin Snyder's Star Fleet Math proofs from scratch (#394 too) — already claimed, not by us, still worth checking",
    date: "2026-07-25",
    status: "proof_claimed",
    summary:
      "Star Fleet Math (Colin Snyder, GPT-5.6 with a custom Lean harness) has " +
      "quietly submitted full proof claims for four open Erdős problems on " +
      "the tracker — ten days before we noticed. We almost shipped these as " +
      "our own unflagged finds, on a triage brief whose search access was " +
      "blocked from seeing the tracker's proof-claims pages. We caught it " +
      "before posting anything: all four (#489, #394, #336, #1188) are " +
      "already on record, zero comments, zero scrutiny. So instead of " +
      "\"we found this,\" here's the honest version — an independent " +
      "from-scratch rebuild of two of the four, on our own compute, as a " +
      "second opinion nobody had given yet.",
    body: `
<p><strong>What actually happened.</strong> We fired a triage brief asking
a GPT-5.6 reasoner to rank four downloadable Lean solution bundles from
Star Fleet Math (starfleetmath.com — a real, named, humbly-framed project:
"proposed solutions," explicit invitation to correct them) before we spent
compute rebuilding any of them. It ranked <a href="https://www.erdosproblems.com/489">#489</a>
and <a href="https://www.erdosproblems.com/394">#394</a> as the strongest
candidates, with an honest caveat: its own tracker access was blocked, so
it "could not honestly certify the live forum as empty." We took that as
license to proceed on the working assumption these were unflagged.</p>

<p><strong>We were wrong, and caught it ourselves before shipping.</strong>
Every erdosproblems.com problem page has three sub-surfaces: the top-level
statement, a general comment thread, and a separate
<code>/forum/thread/N/proof-claims</code> page — a formal submission
mechanism, counted separately as "N claimed proofs" on the top page. We'd
been checking the first two all day. Loading the third for #489 turned up
a full proof claim by Colin Snyder himself, submitted 2026-07-15 —
ten days before today. Same story for #394, #336, and #1188: all four
submitted in one batch that day, all still sitting at zero comments.
Not unflagged. Already-claimed-and-unscrutinized — a smaller, more honest
thing to report.</p>

<p><strong>What we still did, because it's still worth doing:</strong> two
independent from-scratch rebuilds, on Hetzner boxes we controlled, of
Snyder's #489 and #394 claims. For #489 — does
<code>Σ(b_{i+1}−b_i)²/x</code> converge for the gap sequence of a
divisor-sieved set B, when the forbidden set A has |A∩[1,x]| = o(√x)? —
we read the Lean <code>gapSumSq</code> definition by hand first (the
central audit risk: does it use the true next element of B, even past x,
or truncate the gap at the boundary?) and confirmed it's correct. Then a
full rebuild: 8,608/8,608 jobs, and:</p>
<p><code>'Erdos489.erdos489_statement' depends on axioms: [propext, Classical.choice, Quot.sound]</code></p>

<p>For #394 — does Σt₂(n) ≪ x²/(log x)^c for some c>0, and does
Σt_{k+1}(n) = o(Σt_k(n)) for every fixed k≥2, where t_k(n) is the least m
with n | m(m+1)⋯(m+k−1)? — we confirmed the Lean definition correctly
requires <code>0 &lt; m</code> (excluding the degenerate m=0 collapse), then
a full rebuild: 8,664/8,664 jobs, and both target theorems clean:</p>
<p><code>'Research.erdos394_first_target' depends on axioms: [propext, Classical.choice, Quot.sound]<br>
'Research.erdos394_second_target' depends on axioms: [propext, Classical.choice, Quot.sound]</code></p>

<p><strong>One real thing surfaced along the way.</strong> A separate,
third-party comment on #394's proof-claims page (Jeff Pickhardt, with an
"Omniscience Research Agent," 2026-07-23) proves a genuine correction:
the site's stated <em>stronger</em> Erdős–Hall conjecture — that the sum
is o(x²/(log x)^c) for every c &lt; log 2 — is false. You can't take c
past 1/2. Snyder's own claimed c = 1/2048 survives that bound comfortably.
That's real, sourced math, independent of whether Snyder's own claim
holds up to further scrutiny.</p>

<p><strong>What we're doing about it.</strong> No new proof claim, no
"we found this" comment — that would be exactly the overclaim we're
trying not to repeat (see the #1151 correction elsewhere on this site).
What's staged for Patrick, if he wants it: a short corroborating comment
noting an independent third-party Lean rebuild confirms both claims
build clean. Full credit to Colin Snyder for the original construction.
#336 and #1188 remain unverified by us — Pro's own triage flagged real
definitional risk in both (basis "order" conventions for #336, covering-
system canonicalization for #1188) that wants a manual read before any
compute, and given today's correction, they're also already-claimed, not
urgent.</p>
`,
    links: [
      { label: "erdosproblems.com/489", url: "https://www.erdosproblems.com/489" },
      { label: "erdosproblems.com/394", url: "https://www.erdosproblems.com/394" },
      { label: "Star Fleet Math (Colin Snyder)", url: "https://www.starfleetmath.com" },
    ],
  },
  {
    slug: "593-1177-obligatory-triple-systems",
    problemNum: 593,
    title: "#593 and #1177: Eric Li's obligatory-triple-system classification, independently rebuilt from scratch",
    date: "2026-07-25",
    status: "proof_claimed",
    summary:
      "A $500-prize problem (#593, characterize the finite triple systems " +
      "every uncountably-chromatic triple system must contain) plus a " +
      "companion (#1177, three exact-cardinal questions about avoidance " +
      "classes) — both already claimed by Eric Li, already flagged by the " +
      "community as warranting extra scrutiny given his pace of claims. " +
      "We gave it that scrutiny: cloned the repo, built from source, ran " +
      "#print axioms on all 8 component theorems plus the unconditional " +
      "master theorem. Clean.",
    body: `
<p><strong>Not a discovery — targeted scrutiny of an existing, already-flagged claim.</strong>
Both <a href="https://www.erdosproblems.com/593">erdosproblems.com/593</a> (a $500-prize
problem) and <a href="https://www.erdosproblems.com/1177">#1177</a> already show a comment
(Alfaiz, 24 Jun) noting Eric Li's paper claims to resolve them. On #1177's page, Nat Sothanaphan
adds a specific, fair caution: Li is a "3rd year CS undergraduate" who has "claimed to solve
multiple problems on this site in a row, with non-short papers" — not a reason to dismiss the
work, but a reason it deserves more scrutiny than usual before anyone trusts it. Nobody in either
thread had done a full independent rebuild. That's what we did.</p>

<p><strong>The problems.</strong> #593: characterize which finite 3-uniform hypergraphs must
appear in every 3-uniform hypergraph of chromatic number >ℵ₀. #1177: three exact-cardinal
questions about the avoidance classes F_G(κ) (does nonemptiness at ℵ₁ give a bounded-size
witness; can two nonempty avoidance classes fail to share a member; does nonemptiness at one
uncountable cardinal give nonemptiness at every uncountable cardinal). Li's paper
(arXiv:2606.24882) answers all of it — the classification for #593, and yes/no/yes for #1177's
three parts — as a single unconditional theorem with zero hypotheses.</p>

<p><strong>What we actually did.</strong> Cloned Li's repo
(github.com/ericlisg/erdos-593-1177-lean) on a disposable box, built the entire ~8,000-job
project from source against pinned Mathlib, then ran <code>#print axioms</code> on every
individual component (the Erdős–Hajnal odd-girth case, EGH, Reiher, the HK loose-7 case, all
three parts of #1177) and the master theorem:</p>
<pre>'Erdos593.full_resolution_unconditional' depends on axioms:
[propext, Classical.choice, Quot.sound]</pre>
<p class="meta">Every single one clean — no <code>sorryAx</code>, just the standard three. The
repo's own build pipeline runs this same audit automatically; we didn't take that on faith
either, we reproduced the whole thing ourselves, from a clean clone, on infrastructure we
controlled.</p>

<p><strong>What this doesn't settle.</strong> A clean Lean kernel check confirms the formalized
statement is proved — it doesn't confirm the formalization faithfully captures the informal
problem (a live concern named in Nat's own comment, and the right next scrutiny step: read the
Lean statement against the tracker's exact wording line by line, which we haven't done as
carefully as we did the axiom check). And "no human has read this end to end" was Woett's fair
caution on the sibling #768 case — the same applies here.</p>
`,
    links: [
      { label: "erdosproblems.com/593 ($500)", url: "https://www.erdosproblems.com/593" },
      { label: "erdosproblems.com/1177", url: "https://www.erdosproblems.com/1177" },
      { label: "Eric Li, arXiv:2606.24882", url: "https://arxiv.org/abs/2606.24882" },
      { label: "github.com/ericlisg/erdos-593-1177-lean", url: "https://github.com/ericlisg/erdos-593-1177-lean" },
    ],
  },
  {
    slug: "768-sylow-divisor-condition",
    problemNum: 768,
    title: "#768: the Sylow divisor condition — Eric Li's constant, independently rebuilt, now the THIRD clean Lean check",
    date: "2026-07-25",
    status: "proof_claimed",
    summary:
      "Density of integers where every prime factor has a divisor ≡1 mod " +
      "itself — Eric Li's paper pins the exact constant c=1/(2√log2). " +
      "Already independently formalized twice by different people " +
      "(Li himself, and separately JohanLand). We're a third, from-scratch " +
      "check, not the first.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/768">erdosproblems.com/768</a>).
Let A be the integers n where every prime p∣n has some divisor d∣n, d>1, with d≡1 (mod p) — the
"Sylow divisor condition." Erdős showed |A∩[1,N]|/N = exp(−(c+o(1))√(logN·loglogN)) for some
c>0 bounded between the trivial c=1 and c can't-be-improved; the question is the exact constant.</p>

<p><strong>Already flagged, already double-checked — we're a third opinion, not a discovery.</strong>
Eric Li posted this himself on 12 Jul, with a Lean formalization and full disclosure of AI
assistance. Two days later, a different person (JohanLand) independently formalized the same
paper from scratch — without having seen Li's own Lean code — and it also compiled clean,
catching one trivial, non-load-bearing gap in the paper's Lemma 6.3 that doesn't affect the
result. That's real, working peer scrutiny already in public. What we added: a third
independent build, on infrastructure neither of them touched.</p>

<p><strong>What we did.</strong> Cloned github.com/ericlisg/erdos768-lean fresh, built the whole
~8,000-line project from source (including its real analytic input, MediumPNT from
PrimeNumberTheoremAnd — a real, substantial prime-number-theorem dependency, not a stub), then
ran our own <code>#print axioms</code>:</p>
<pre>'Erdos768.erdos_768' depends on axioms:
[propext, Classical.choice, Quot.sound]</pre>
<p class="meta">Clean. The repo's own build already enforces this via a hard-coded
<code>#guard_msgs</code> check that fails the build on any axiom mismatch — we independently
confirmed the same result outside that guard.</p>

<p><strong>Constant:</strong> c = 1/(2√log2) ≈ 0.849, resolving the open part of #768.</p>
`,
    links: [
      { label: "erdosproblems.com/768", url: "https://www.erdosproblems.com/768" },
      { label: "Eric Li, arXiv:2606.24872", url: "https://arxiv.org/abs/2606.24872" },
      { label: "github.com/ericlisg/erdos768-lean", url: "https://github.com/ericlisg/erdos768-lean" },
    ],
  },
  {
    slug: "796-multiplicative-representation",
    problemNum: 796,
    title: "#796: not unflagged either — Gajjala's own proof claim was already on the tracker, and there's a second, independent, competing one",
    date: "2026-07-25",
    status: "proof_claimed",
    summary:
      "g₃(n): the largest A⊆[n] where every integer has at most two " +
      "representations as a product of two elements of A. We first shipped " +
      "Rishikesh Gajjala's construction as unflagged; it wasn't — his own " +
      "proof-claims submission was already on the tracker since 15 July, " +
      "and so was a separate, independent, earlier claim by Colin Snyder " +
      "(Star Fleet Math) giving a sharper exact constant. Our from-scratch " +
      "rebuild of Gajjala's proof still stands (with a real sorry found, " +
      "traced, and confirmed harmless) — Snyder's competing claim is not " +
      "yet independently checked by us.",
    body: `
<p><strong>We got this one wrong the same way as #489/#394/#336/#1188 elsewhere on this site</strong>
— checked erdosproblems.com/796's general comment thread (which really does only cover a January
2026 statement-typo fix) and missed the separate <code>/forum/thread/796/proof-claims</code> page,
where the formal proof-claim submissions actually live. That page shows two, both dated
2026-07-15: Rishikesh Gajjala's own submission of the exact repo we rebuilt (01:48 UTC), and — a
few hours <em>earlier</em> — a full proof claim by Colin Snyder using "GPT 5.6 (custom harness)",
the same Star Fleet Math project behind the #489/#394 entry on this site. Snyder's claim is more
precise: an explicit closed form (the constant equals the Mertens constant plus an explicit
variational limit), against Gajjala's claim of existence of some constant between 1 and 15. Both
independent, both already on record ten days before we looked. Not a discovery on either count.</p>

<p><strong>The problem.</strong> For A⊆[n], every integer having at most two representations as
a=a₁a₂ with a₁<a₂∈A caps how large A can be. Erdős's classical asymptotic gives the leading term;
the open question is the exact second-order constant.</p>

<p><strong>What still stands from our original work:</strong> a genuine from-scratch rebuild of
Gajjala's proof, with a real complication found and correctly triaged, not glossed over. Our
first build attempt used the repo's default <code>lake build</code> target, which turned out to
only compile the problem statement, not the actual proof (their real CI passes
<code>Erdos796.FullProof</code> explicitly — caught by reading their CI config, not by luck).
Redone the right way, the build log showed a genuine warning: <code>declaration uses \`sorry\`</code>,
inside a Rosser–Schoenfeld file in the PrimeNumberTheoremAnd dependency. We ran
<code>#print axioms</code> individually on every one of the 7 official release theorems —
including the actual target, <code>erdosProblem796</code> — using Lean's strictest
<code>--trust=0</code> kernel mode, exactly matching the repo's own audit script:</p>
<pre>'Erdos796.erdosProblem796' depends on axioms:
[propext, Classical.choice, Quot.sound]</pre>
<p class="meta">All 7 clean, including the target. The sorry lives in a part of the
PrimeNumberTheoremAnd library that this specific proof's dependency chain never actually
touches — confirmed, not assumed.</p>

<p><strong>What we haven't done:</strong> independently verified Snyder's separate, sharper claim.
Given his claimed exact constant (Mertens constant plus a variational limit) is a strictly
stronger statement than Gajjala's coarse existence bound, if both proofs are correct they're
compatible — but we haven't rebuilt Snyder's bundle the way we rebuilt Gajjala's, so we're not
vouching for it. Flagging that honestly rather than letting the "genuinely unflagged" framing we
originally shipped imply we'd checked everything relevant.</p>
`,
    links: [
      { label: "erdosproblems.com/796", url: "https://www.erdosproblems.com/796" },
      { label: "github.com/rishigajjala/erdos-796-lean", url: "https://github.com/rishigajjala/erdos-796-lean" },
    ],
  },
  {
    slug: "458-lcm-consecutive-prime-gap",
    problemNum: 458,
    title: "#458: is [1,...,pₖ₊₁−1] always less than pₖ·[1,...,pₖ]? A sharper threshold, and the conjecture holds through 10²⁰",
    date: "2026-07-25",
    status: "in_progress",
    summary:
      "Erdős and Graham call this 'almost certainly' true but 'beyond our " +
      "ability' to prove. New reciprocal-exponent budget sharpens exactly " +
      "what a counterexample would need to contain, and (conditional on a " +
      "real distributed prime-gap computation) the conjecture holds for " +
      "every gap through 10²⁰. First problem this session came from a " +
      "fresh, self-directed scout rather than a shared transcript.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/458">erdosproblems.com/458</a>,
status FALSIFIABLE, 0 claimed proofs, no current worker). Let [1,...,n]
denote lcm(1,...,n). For consecutive primes pₖ<pₖ₊₁, is
[1,...,pₖ₊₁−1] < pₖ·[1,...,pₖ] always true? Erdős and Graham themselves
say this is "almost certainly" true but the proof is out of reach for two
named reasons: ruling out two primes q with pₖ<q²<pₖ₊₁ (essentially
Legendre's conjecture), and small-prime edge cases.</p>

<p><strong>How this one got picked.</strong> Different from every other
entry today — this wasn't a shared transcript. We asked an agentic coding
model (Codex, GPT-5.6 Sol at max reasoning effort) to scout
erdosproblems.com itself for a problem matching one of our two proven
attack shapes (valuation-transport across consecutive-integer windows, or
Pell-reducible consecutive-product equations) and just go attempt it.
It surveyed nine candidates, gave a specific reason for rejecting each
(too crowded, doesn't actually reduce to the shape it looks like, active
workers already attached), and picked #458.</p>

<p><strong>The result: an exact valuation-transport identity</strong>
[1,...,pₖ₊₁−1] / [1,...,pₖ] = Q(p,r), the product of every prime q with a
power q^a strictly between p and r (a≥2, since no prime itself can sit in
a prime gap). The question is just whether Q(p,r) < p always. A
"reciprocal-exponent budget" sharpens this: each such event q^a<r forces
q<r^(1/a), so a counterexample needs total reciprocal weight
Σ1/a > log p / log r — meaning one square (weight 1/2) plus one cube
(weight 1/3) is already impossible once p>32, by Bertrand's postulate
alone. Pushed further: whenever the gap is short (r−p≤4√p, the regime
that actually matters), a counterexample needs either one square plus two
cubes-or-higher, or five-plus higher powers with no square at all — a
real, proven structural theorem, not a heuristic.</p>

<p><strong>And, conditionally, the conjecture holds through 10²⁰.</strong>
Feeding in a real external input — the Prime Gap List project's
distributed computation that every prime gap below 10²⁰ has length at
most 1854 (the peer-reviewed record only reaches 4×10¹⁸, Oliveira e
Silva–Herzog–Pardi 2014, so this leans on a community computation, not a
refereed one) — the structural theorem above closes every gap in that
entire range.</p>

<p><strong>We verified every number independently, with our own code,
not theirs.</strong> 73³=389017 and 5⁸=390625 (the closest pair of
higher prime-power thresholds below 10²⁰, distance 1608) — confirmed,
and 389023 sitting strictly between them is genuinely prime, breaking
any gap that could contain both. The p=37-vs-p=31 threshold where the
single-square-plus-cube bound starts working — confirmed exactly where
predicted. The extremal small case, gap (7,11): Q=6, quotient 6/7 —
recomputed directly via lcm(1..10)/lcm(1..7)=2520/420=6, matches. Then,
independent of any of their code, we wrote our own valuation-transport
scanner from scratch and checked 41,537 consecutive-prime gaps up to
500,000 — zero failures, consistent with their own from-scratch scan
through 10⁷. Both citations (Prime Gap List project, Oliveira e Silva et
al., Math. Comp. 83 (2014)) are real.</p>

<p><strong>What's still open.</strong> This doesn't close the problem —
it isolates it more sharply. Two genuine remaining obstructions, both
named honestly rather than hidden: ruling out two prime squares in one
gap in general needs something like Legendre's conjecture (exactly what
Erdős and Graham flagged), and ruling out mixed higher-power near-misses
in general is a Pillai/Hall-type close-perfect-powers problem — no single
finite modular cover handles it the way our Pell-equation wins have.</p>
`,
    links: [
      { label: "erdosproblems.com/458", url: "https://www.erdosproblems.com/458" },
      { label: "Prime Gap List project", url: "https://primegap-list-project.github.io/fully-analyzed/" },
      { label: "Oliveira e Silva–Herzog–Pardi, Math. Comp. 83 (2014)", url: "https://doi.org/10.1090/S0025-5718-2013-02787-1" },
    ],
  },
  {
    slug: "122-repeated-values-arithmetic-functions",
    problemNum: 122,
    title: "#122: does n+f(n) pile up on the same values, for (almost) every slow-growing f?",
    date: "2026-07-25",
    status: "in_progress",
    summary:
      "For which f does n+f(n) hit some output range far more often than " +
      "chance, for every F growing slower than f? Confirmed: Maynard's " +
      "2016 clustering theorem really does build exact, verifiable " +
      "collisions of n+τ(n); the real 1985/1997 Erdős–Pomerance–Sárközy " +
      "mechanism is reconstructed correctly; and the naive τ generalization " +
      "of it fails for a precise, provable algebraic reason. Round 5: a " +
      "genuinely new result EPS never published — for every fixed m, " +
      "infinitely many y have at least m representations y=n+τ(n), " +
      "rigorous modulo a real 1985 theorem, independently reverified.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/122">erdosproblems.com/122</a>,
OPEN, 0 claimed proofs — three people currently working on it). For which
number-theoretic f is it true that for every F with F(n)/f(n)→0 almost
everywhere, there are infinitely many x where the count of n with
n+f(n)∈(x,x+F(x)), divided by F(x), goes to ∞? Erdős, Pomerance and
Sárközy proved a concrete clustering statement for f=ω(n) (number of
distinct prime factors) and reported — without publishing details — that
the same works for f=τ(n) (the divisor function), and probably fails for
f=φ(n) or σ(n).</p>

<p><strong>Three real, separable findings, none of them the full
theorem.</strong> (1) Maynard's 2016 prime-clustering theorem really does
give an explicit, verifiable construction of arbitrarily large exact
fibers of n+τ(n) — a CRT-forced system of affine forms where forcing
divisors with prescribed τ-values and then hitting several simultaneous
primes creates exact collisions, checked algebraically end to end.
(2) The actual published EPS mechanism for ω(n) isn't "shifts don't
change ω(n) much" (a plausible-sounding wrong guess) — it's a CRT
construction that <em>programs</em> a forced additive contribution to
ω(n+i) that exactly cancels the offset i, with a controlled statistical
residual doing the rest. (3) That mechanism breaks for τ(n) for a precise
algebraic reason: ω is additive over coprime factors, τ is multiplicative
— so the same offset-cancellation trick that works by addition for ω
needs multiplication for τ, and the natural probabilistic estimate
(normal order of log τ) becomes useless once you exponentiate back to τ
itself. EPS's own printed remark that τ works "with a little more
difficulty" is real, but the details were never published, and a
plausible reconstruction of what they might have meant runs into three
concrete new gaps, honestly named rather than papered over.</p>

<hr>

<p><strong>Round 2, same day: the divisor-packet gap is essentially
closed.</strong> Of the three named gaps, the first — realizing many
prescribed τ(d)=a values cheaply enough for the CRT construction to stay
useful at scale — turns out to have a clean answer. Powers of two suffice
for the collision mechanism itself: a sparse packet using targets
a=2⁰,2¹,...,2^(R−1) has an exact-valuation CRT modulus of only
exp((2+o(1))R²log R), small enough to let R grow like √(log x)/loglog x
while the modulus stays x^o(1) — genuinely large R, not just a fixed small
one. If instead every value a=1,...,R is needed (a more compact packet),
the modulus is exp(Θ(R²)) — both an explicit construction achieving this
and a matching lower bound (forced by prime targets, since τ(d)=ℓ prime
forces d=q^(ℓ−1) with no way around it) are proven. Verified independently
end to end, not just algebra on paper: an explicit 3-row power-of-two
collision (474381+{28,24,16}, all landing on 474413 with τ=4,8,16) and a
4-row compact collision (383976193+{16,12,8,4}, all landing on 383976213
with τ=4,8,12,16) — recomputed both from scratch with an independent
divisor-count routine, not the source's own verifier, exact match on
every number. What's left of the three original gaps: the uniform
exact-ω distribution estimate (still open, needs something like a
Sathe–Selberg result uniform in a growing modulus) and the exceptional-set
robustness question.</p>

<p><strong>We checked the checkable parts ourselves.</strong> Built a
small real instance of the exact-collision construction from scratch —
k=(4,6,8), primes (5,7,11), d_i=p_i^(k_i/2−1)=(5,49,1331), verified
τ(d_i) really equals k_i/2 exactly, ran CRT for b and D, then searched
for t where multiple L_i(t) are simultaneously prime. <strong>The very
first hit, at t=0</strong>: y=81199, with n=81193 and n=81191 both
independently satisfying n+τ(n)=81199 — a genuine, verified double
collision, not asymptotic, not simulated. Also directly tested the
paper's general density constraint: sieved τ(n) for n up to 5,000,000,
confirmed Σ_{y≤X} r_τ(y) = 4,999,983 (essentially X, as claimed) and that
the density of {y: r_τ(y)≥M} stays comfortably under 1/M at every M we
checked (found real fibers up to size 7 in that range). Every citation
(Maynard, Compositio Math 152 (2016), 1517–1554; Erdős–Pomerance–Sárközy
I, J. Number Theory 21 (1985); EPS IV, Ramanujan J. 1 (1997)) verified
directly against Crossref, exact match on title/venue/volume/pages.</p>

<p><strong>A real source-hygiene catch, resolved.</strong> The source
chat flagged that older archived versions of this problem's statement
may have had the inequality direction reversed (f/F→0 vs. F/f→0) and
couldn't access the live tracker to check. We could: the page as it
stands today uses F(n)/f(n)→0, matching what the analysis assumed — so
that specific worry is resolved, though the original 1997 Erdős source
text itself still hasn't been independently re-read by us or the chat.</p>

<p><strong>What's still open.</strong> No proof of the general
arbitrary-F statement, not even reconstructed for f=ω. A fixed Maynard
tuple provably can never give positive density of collision centers (its
centers sit inside a finite union of prime-value sequences, density
zero) — real news, but it also means the eventual proof needs a genuinely
new averaged construction over a growing family of systems, not a
stronger single application of Maynard. Of the two named next-step
lemmas, the divisor-packet efficiency question is now answered (see
below) — the uniform exact-ω residual lemma is still open.</p>

<hr>

<p><strong>Round 3, same day: the picture sharpens further — two of the three
gaps dissolve, and the third turns out to be a real structural wall, not just
a missing estimate.</strong> Gap B gets a cleaner closure than round 2's
powers-of-two packet: an "odd-part subset code" — target τ-values
2^j·(product of a subset of the first few odd primes) — gives exponentially
many distinct, cheaply-realized divisor-count values with CRT modulus only
X^o(1), because the 2-adic part recovers j and unique factorization of the
odd part recovers the subset. We built a small real instance independently
(2 codewords, targets τ=4 and τ=24) and searched the actual CRT residue
class for a genuine hit: at n=9437, both 9458 (τ=4) and 9438 (τ=24) land on
the same value 9462 — a real, searched, not simulated collision, confirming
the underlying cancellation lemma works exactly as claimed.</p>

<p><strong>Gap A turns out to have been asking for more than necessary.</strong>
The original framing wanted joint control over many residual progressions
simultaneously — genuinely hard. But a first-moment argument only needs each
progression's success counted <em>separately</em> and then summed — no joint
distribution needed. Claudia Spiro's real 1985 paper ("Extensions of some
formulae of A. Selberg," verified via a real citation search — Intl. J. Math.
Math. Sci., pp. 283–302) gives exactly the arithmetic-progression-uniform
exact-ω estimate this simpler version needs.</p>

<p><strong>Gap C is the real wall.</strong> For this specific
pairwise-coprime-support construction, the candidate collision centers are
provably too sparse to survive an adversarial density-zero exceptional set
for F — not a missing estimate that better bookkeeping could supply, a
structural limit of building the construction from one preselected CRT
code. That's honest, useful news: it names precisely why this whole line of
attack can't reach the problem's actual arbitrary-F statement, redirecting
future effort toward a genuinely different (averaged, multi-code) construction
rather than sharpening this one further.</p>

<hr>

<p><strong>Round 4, same day: Gap C's wall gets a precise shape, and a concrete
redirection — checked, not just asserted.</strong> The wall isn't "one residue
class is too thin" — it's sharper. Varying the CRT code (choice of shift C)
only ever produces an F(x)-fold <em>backward shadow</em> of the same collision
centers; it creates no new center progressions. And a genuinely universal
bound applies regardless of construction: since R(y) := #{n: n+τ(n)=y}
satisfies Σ_{y≤X} R(y) ≤ X (trivial — n+τ(n)>n forces n<X), any packet of size
K that must beat a window of length H by factor K/H can live on density at
most H/K. We checked this arithmetic ourselves: it's exactly Markov's
inequality applied to a genuinely trivial identity, not a deep theorem, but it's
the right one — a growing packet concentrated at one center is structurally
forced onto a density-zero set, no matter how the CRT code is built.</p>

<p><strong>What does vary usefully, and what doesn't.</strong> At the raw
squarefree-divisibility level, varying which support primes hit which targets
really can build a density-(1−o(1)) union (an explicit occupancy theorem, with
pairwise-negative-correlation second-moment bound) — <em>we re-derived and
checked the small worked example ourselves</em>: targets t₁=4, t₂=8, support
pool {5,7,11,13}. Code assigning 5↔4, 7↔8 gives y≡29 (mod 35); at y=239,
239−4=235=5·47 (τ=4) and 239−8=231=3·7·11 (τ=8) — both true, independently
recomputed. Swapping the assignment gives y≡18 (mod 35); at y=263, 263−4=259=
7·37 (τ=4) and 263−8=255=3·5·17 (τ=8) — also both true. The claimed union
density 1−2a+b=146/1001≈0.145854 (a=576/1001, b=297/1001, from the exact
Euler products over {5,7,11,13}) checks out digit-for-digit against direct
computation. But this occupancy trick doesn't rescue the actual odd-part
subset code Gap B/C need: the total reciprocal mass of viable prime-power
supports across all odd target primes is finite (Σ_q Σ_p 1/p^(q−1) < 3/4, a
genuine convergent series, checked against the exponent-1-vs-exponent-≥2
divergence/convergence boundary), so the full K-word subset code's viable
density collapses as exp(−Ω(K log K)) — exponentially, not polynomially, no
matter how many codes or labels are varied.</p>

<p><strong>The redirection is concrete, not hand-wavy.</strong> The right new
target isn't "land a τ-sized packet at one center" — it's, for each fixed
amplification M and on a dyadic scale where F(x)≍H, a positive-density set of
x with Σ_{h=1}^H R(x+h) ≥ MH. The same output-mass identity that kills the
one-center approach only imposes a sharp ceiling here (density ≤ 1/M + o(1)),
not impossibility — this formulation is a real, still-open target, needing a
genuinely different (Maynard-style, many-shift, positive-density) selection
theorem rather than one more preselected CRT code. Literature check: the
relevant tools (Chung–Erdős/Paley–Zygmund, Turán sieve, Kochen–Stone,
Davenport–Erdős, Gallagher's larger sieve, Tao–Teräväinen's τ/ω/Ω
correlations) are all real and correctly characterized as adjacent-but-not-
sufficient — none is a hidden escape hatch for the current construction, which
is honest since we'd rather report "no known shortcut" than manufacture one.</p>

<hr>

<p><strong>Round 5, next day: the honest-fallback target from the original brief actually lands —
a genuinely new theorem, not just a sharper diagnosis of the wall.</strong> Rounds 3–4 explained
precisely why this construction can't reach the full arbitrary-F statement. What we asked for as a
consolation prize, if that stayed out of reach, was a weaker but still-new EPS-style theorem: for
<em>every</em> fixed m, are there infinitely many y with at least m representations y=n+τ(n)? Erdős,
Pomerance, and Sárközy never published even this weaker form for τ(n) (only for ω(n)). This round
gets it: <strong>g_τ(y) := #{n : n+τ(n)=y} satisfies g_τ(y) ≥ c·√(loglogX) / logloglogX for some
y∈[X,3X], for an absolute constant c>0 and all sufficiently large X — rigorous modulo Claudia
Spiro's real 1985 theorem</strong> (Spiro, "Extensions of some formulae of A. Selberg," Intl. J.
Math. Math. Sci. 8 (1985), 283–302 — a real paper by a real number theorist, Erdős number 1,
independently confirmed via citation search; the specific uniform arithmetic-progression estimate
it's cited for matches the paper's actual subject, though we couldn't get past Wiley's paywall to
check the exact theorem number's constants verbatim). Since the bound diverges, g_τ is unbounded,
which is exactly the new EPS-I-style corollary: for every fixed m, infinitely many y have at least m
representations as n+τ(n).</p>

<p><strong>The return itself had an internal inconsistency, caught and resolved before shipping,
not papered over.</strong> The document stated its own headline bound two different, NOT
equivalent ways in different sections — one phrasing that would have overstated the result by a
diverging factor. We re-derived the exponent directly from the construction's own earlier parameter
choices (the modulus-size accounting from Gap B, the packet-count K from Gap A's averaging) rather
than trusting either rendering, and confirmed the weaker, correct form above is the one the proof
actually supports.</p>

<p><strong>Independently verified with real numbers, not just re-read.</strong> Built three fresh
CRT-cancellation certificates from scratch (none copied from the source): the source's own 4-fold
example (n=1912865606704203022636, offsets giving τ=4,12,20,60, all colliding at n+61) refactored
independently, all four τ-values exact; its small 3-fold example (n=4543160725620, τ=6,10,14,
colliding at n+15) refactored, exact; and a wholly independent instance we built ourselves (fresh
residuals, fresh CRT modulus, searched the resulting progression cold) — found n=183033, where
n+5=183038=2·71·1289 (τ=8 ✓) and n+1=183034=23²·346 (346=2·173, τ=12 ✓) both collide at n+13,
confirming this is a genuine density phenomenon in the progression, not a coincidence special to
the source's hand-picked numbers. Also independently re-verified the odd-part subset code
construction (5 fresh instances, different primes than the source used) and the "powers of two
alone can't scale" size bound (brute-forced the combinatorial minimum against the closed-form
estimate for 24+ cases, exact match every time) — zero discrepancies found anywhere in the load-
bearing math.</p>
`,
    links: [
      { label: "erdosproblems.com/122", url: "https://www.erdosproblems.com/122" },
      { label: "Maynard 2016, Compositio Math (DOI)", url: "https://doi.org/10.1112/S0010437X16007296" },
      { label: "Erdős–Pomerance–Sárközy IV, Ramanujan J. 1997", url: "https://doi.org/10.1023/A:1009723712317" },
      { label: "Spiro 1985, Intl. J. Math. Math. Sci. (DOI)", url: "https://doi.org/10.1155/S016117128500031X" },
    ],
  },
  {
    slug: "44-sidon-density-completion",
    problemNum: 44,
    title: "#44: can any finite Sidon set be completed to near-optimal density? A real deletion barrier, not just a stalled attempt",
    date: "2026-07-25",
    status: "in_progress",
    summary:
      "Given any finite Sidon set A, can you always extend it to a bigger " +
      "one of near-(1−ε)√M density? A quantifier-correct construction " +
      "reaches 1/√2, full density-1 for |A|≤2 (and |A|=3 via a named " +
      "unpublished proof), and a proof that the obvious repair strategy " +
      "(patch a perfect difference set) is structurally dead for seeds " +
      "like Alexeev–Mixon's {1,2,4,8,13}. Round 2: the two |A|=4 patterns " +
      "that provably embed in no Singer difference set turn out to embed " +
      "cleanly in a different classical family instead — Singer failure " +
      "wasn't the wall it looked like. Round 4: the round-3 obstruction " +
      "sets do embed in Sidon spaces (rebuilt and independently verified, " +
      "including a real density-value error caught along the way), but a " +
      "cited nonexistence theorem shows the standard construction family " +
      "is empty exactly where density-one completions would need to live. " +
      "Round 5: cubic Bose–Chowla doesn't restore coverage either — a " +
      "clean, verified structural negative. Round 6: two reasoners " +
      "working independently converge exactly, and a fact Round 4 left " +
      "unverified — zero binary critical Sidon spaces at dimension 5 — " +
      "is now genuinely triple-checked.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/44">erdosproblems.com/44</a>,
OPEN, 0 claimed proofs — someone's actively working on formalizing it
right now). Given any finite Sidon set A ⊂ {1,...,N}, does every ε>0
admit an M and a completion B ⊂ {N+1,...,M} with A∪B Sidon and size at
least (1−ε)√M? Related to problems #329 and #707 — a positive answer to
#707 would imply this, which would imply #329.</p>

<p><strong>What's new here isn't a solve — it's a real obstruction,
proven, not just observed.</strong> The natural attack is: take a huge
Singer perfect difference set (the classical near-optimal Sidon
construction, density ~1/√M), delete whatever collides with your fixed
seed A, keep the rest. The chat proves this can't work for certain seeds:
an external point not already inside the difference set forces Θ(q)
genuine integer collisions, and deleting one point can repair at most 4
of them — so at least (1/16−o(1))q points have to go. For Alexeev–Mixon's
{1,2,4,8,13}, which provably embeds in <em>no</em> perfect difference set
at all, that's fatal to the whole sparse-repair template. A different,
linearly-far construction would be needed.</p>

<p><strong>We rebuilt the actual mechanism from scratch — not just the
citations.</strong> Implemented a genuine Singer perfect difference set
via GF(q³) arithmetic (trace-zero coset construction), verified it's
really λ=1 (every nonzero residue represented as a difference exactly
once) for q=2,3,5,7. Tested the |A|≤2 embedding claim directly: zero
failures across all 56 possible target differences at q=7. Tested the
deletion-barrier mechanics (Steps 1–4 of the proof): x↦f_x really is a
permutation, multiplicity per point really caps at 2, total appearances
per point really caps at 4 — all confirmed exactly, not approximately.
And we reproduced their actual headline number independently: scanning
all 2,052 affine copies of the q=7 Singer set (matches their count
exactly — φ(57)=36 units × 57 shifts) against the normalized
Alexeev–Mixon seed, minimum additional deletions needed = 1, found via
our own from-scratch search (u=2, t=22), not copied from their result.</p>

<p><strong>Citations, checked directly, not trusted:</strong>
Alexeev–Mixon (arXiv:2510.19804, the non-embedding result), Tong Niu's
withdrawn size-4 follow-up (arXiv:2604.25214), O'Bryant's July 2026
thickness paper confirming Ruzsa's 1/√2 is still the infinite-Sidon
record (arXiv:2606.28651), Eberhard–Manners' dense-Sidon structure
conjecture (arXiv:2107.05744) — all real. Will Sawin's unpublished
|A|=3 proof, pulled directly from the MathOverflow API rather than
trusted secondhand: accepted answer, real, uses Singer's construction +
Weil's Riemann Hypothesis for curves + a primitive-root sieve, exactly as
described — including Peter Mueller's follow-up answer, also real.</p>

<p><strong>What's still open.</strong> No proof and no counterexample.
The |A|=3 case leans on Sawin's algebraic-geometric estimates, which
weren't independently re-derived here (flagged honestly in the source).
The deletion barrier only rules out sparse edits of a single perfect
difference set — it says nothing about a genuinely different, dense
construction built around the seed from the start. Alexeev–Mixon-style
forbidden seeds are the most plausible counterexample candidates but
calling them actual counterexamples to #44 would be an overclaim right
now.</p>

<hr>

<p><strong>Round 2, same day: the two size-4 "forbidden" patterns embed
after all — just not via Singer.</strong> Peter Mueller's MathOverflow
answer named two specific |A|=4 sets, {0,1,3,11} and {0,1,4,11}, that
provably embed in no Singer/Desarguesian perfect difference set for any
q. That sounded like a real wall. It wasn't — it was specific to Singer.
Both patterns embed cleanly and elementarily into a completely different
classical near-optimal Sidon family, Bose–Chowla rulers (built from a
primitive root of a quadratic extension field rather than a projective
plane). {0,1,3,11} embeds via F₅ (T=−1, D=2); {0,1,4,11} via F₂₃ (T=7,
D=11), giving a 23-element modular Sidon set with the target sitting
exactly as its own prefix.</p>

<p><strong>We rebuilt every one of these constructions from scratch,
independent of the transcript — every single number matched.</strong>
Implemented the Bose–Chowla recurrence directly (u_{k+2}=Tu_{k+1}−Du_k
over F_q), verified z has order exactly q²−1 (genuine primitivity, not
just "discriminant is a non-residue") for both worked cases, and
reproduced the full 23-element F₂₃ ruler digit-for-digit — including the
specific primitivity certificates z¹⁷⁶=4+2z, z⁴⁸=6, z²⁶⁴=−1. Verified
both independent Ruzsa–Lindström witnesses (6-mark and 16-mark rulers)
and every resultant/factorization in the paper's negative result about
why the Ruzsa family specifically can't be scaled up (2016=2⁵·3²·7,
197676=2²·3²·17²·19) — exact matches throughout.</p>

<p><strong>The big claim — checked, with a real self-caught mistake
along the way.</strong> The source exhaustively checked all 1,035 Sidon
quadruples {0,1,a,b} for 2≤a<b≤50 and found Bose certificates for 1,030
of them (5 genuine exceptions, all trivially solvable by the empty
extension since their endpoints are small). We reproduced this
independently — and initially got a different exception list, missing
one non-trivial case and including two extra ones. Digging in: our first
pass forgot to check primitivity of the root, only irreducibility — once
we added that check, our two "extra" quadruples turned out to be false
positives (real prefix match, provably non-primitive root, correctly not
a valid certificate), and extending our search range to q≤450 turned up
the missing non-trivial case at q=157. Corrected, our count landed on
exactly 1,030 certificates and exactly their same 5 exceptions:
{0,1,3,7}, {0,1,3,9}, {0,1,4,12}, {0,1,4,13}, {0,1,3,14}. The scope
caveats are the same as round 1: this proves the two literal named
instances and a broad finite survey, not all translations, dilations, or
the general |A|=4 case.</p>

<hr>

<p><strong>Round 3, same day: we asked whether every finite Sidon set embeds in SOME classical
near-optimal family — and the answer is no, with an explicit, machine-verified counterexample.</strong>
Round 2 raised an obvious question: Singer failed for two size-4 patterns but Bose–Chowla rescued
both — is there a short list of classical families (Singer, Bose, Erdős–Turán, Spence–Ruzsa,
Hughes–Cilleruelo — Eberhard–Manners' full catalog of Desarguesian projective-plane templates)
that together cover every finite Sidon set? We fired this as a real brief. The answer: <strong>the
exact union-of-families conjecture is false</strong>, and it's false already at 5–6 points.</p>

<p><strong>Three explicit obstruction sets, found by an algebraic sieve and checked against every
characteristic at once, not case by case.</strong> A₀={0,1,4,6,20} has no degree-2 Bose–Chowla
embedding in <em>any</em> finite field, proved by an explicit Bézout identity over the integers —
an identity like that holds after reduction mod every prime simultaneously, so this isn't a
per-characteristic case analysis, it's a single certificate closing all of them at once.
A*={0,1,3,11,15} simultaneously defeats Singer (via Mueller's known {0,1,3,11} obstruction), Bose,
and the Spence–Ruzsa construction. A**={0,1,3,11,15,20} adds Hughes–Cilleruelo and Erdős–Turán to
that list — a single 6-point Sidon set that embeds in <em>none</em> of the five standard
Desarguesian families.</p>

<p><strong>We independently re-derived the actual polynomial algebra, not just read it.</strong>
Rebuilt the recurrence F_n(T,D) from the stated definition and confirmed it matches their closed
forms through F₆. For A₀: substituted D=T²+T+1, confirmed f₆(T)=−T⁴−2T³−2T²+1 factors as
−(T+1)(T³+T²+T−1) exactly, confirmed f₂₀ mod f₆ = 8T³+21T²+28T+16 exactly, and confirmed the
Bézout identity (−24T−31)f₆+(−3T²−2T+2)(f₂₀ mod f₆) = 1 exactly — the actual proof. For A*: verified
F₁₁(−1,D) and F₁₅(−1,D) factor exactly as claimed, verified the characteristic-17 gcd computation
digit for digit. For A**'s Hughes–Cilleruelo exclusion: verified H₃'s factorization, verified q₁₁
and q₁₅ are exactly the non-degenerate factors of H₁₁ and H₁₅, confirmed their resultant is exactly
17⁶, and confirmed the final mod-17 Bézout certificate closes the argument. Every one of these
exact.</p>

<p><strong>One real arithmetic slip, found and correctly triaged, not load-bearing.</strong> The
Spence–Ruzsa exclusion for A* states "(−2)¹⁵−1−15(−3) = −32724 ≡ 0 (mod 7)" and calls this a
contradiction. We recomputed independently: −32724 ≡ 1 (mod 7), not 0. The stated congruence is
simply wrong — but the actual value being nonzero is exactly what the argument needs (a genuine
mismatch at n=15 in the one surviving characteristic from n=11, which is the real contradiction);
if the value really were 0 as written, that would undermine the exclusion, not support it. So the
final claim (A* excludes Spence–Ruzsa) still holds — the source just mis-stated its own
intermediate number. Flagging this plainly rather than silently fixing it.</p>

<p><strong>What this doesn't prove</strong> — named honestly in the source: A** could still avoid
the five templates yet embed in a non-Desarguesian projective plane, a planar-function family, or
(most importantly for #44 itself) a large classical host after deleting a bounded number of
points — the deletion-barrier question from round 1 is untouched by this. A literature sweep
(Cilleruelo–Nathanson, Forey–Fresán–Kowalski real per Kowalski et al., Hulak–Ramos–de Queiroz,
Bailleul–Riblet, all verified real) found no prior paper claiming universal family coverage either
— so this closes a real gap, not a strawman. The proposed next target: Roth–Raviv–Tamo's
<em>Sidon spaces</em> (arXiv:1705.04560, real, verified) — higher-dimensional subspaces with
unique factorization rather than one-dimensional Bose lines, which get the parameter count right
where higher-degree Bose provably doesn't (h>2 kills density outright: q^(1−h/2)→0).</p>

<hr>

<p><strong>Round 4, same day: the proposed next target lands a real answer, plus a genuinely
sharper open problem.</strong> Do A₀ and A** — the two round-3 obstruction sets that beat all five
Desarguesian families — embed in Sidon spaces instead? Yes, both, explicitly. But Sidon spaces
can't yet deliver the density-one completion #44 actually wants, and the reason why is now precise
rather than vague.</p>

<p><strong>We independently rebuilt both explicit constructions from scratch, in a genuine field
implementation, not just checked the arithmetic on paper.</strong> For A₀={0,1,4,6,20}: built
F₂¹² via the exact stated polynomial (confirmed irreducible <em>and</em> primitive ourselves), took
U₀ = span{1, α¹⁰¹, α⁴⁰⁴, α⁶⁰⁶, α²⁰²⁰}, confirmed it's genuinely 5-dimensional, and ran an exhaustive
pairwise-product check over all 31 nonzero elements to confirm the Sidon property directly — not
assumed. The resulting 31-element cyclic Sidon set in Z/4095Z matched the source's list exactly,
element for element, and 101·A₀ = {0,101,404,606,2020} landed inside it exactly as claimed. Same
full rebuild for A**={0,1,3,11,15,20} in F₂¹³ (H=663): confirmed the claimed relation
1+α⁶⁶³+α¹⁷⁵⁴+α⁵⁰⁶⁹=0 exactly, confirmed the 5-dimensional Sidon property exhaustively, and matched
their 31-element exponent set exactly, including 663·A** landing inside it.</p>

<p><strong>A real error, caught by re-deriving the actual arithmetic instead of trusting the
summary line.</strong> The source reports the resulting densities as K/m ≈ 0.4844 (for A₀) and
≈ 0.3425 (for A**). Both are wrong. With K=31 and m=4095, K/m = 0.00757 — not 0.4844. With K=31 and
m=8191, K/m = 0.00378 — not 0.3425 (off by a factor of ~64 and ~90 respectively; we couldn't
reconstruct where either number actually came from). This doesn't touch the underlying point — if
anything it's stronger evidence for it, since the true densities are even smaller than claimed, and
"enormous embedding flexibility, awful asymptotic density" was already the conclusion being drawn.
Flagging it the same way as the round-3 arithmetic slip: found, checked, doesn't change the
verdict, still worth naming plainly.</p>

<p><strong>Why Sidon spaces don't (yet) close #44 for these seeds.</strong> Density-one completions
are proven to require an exact "binary critical" regime (field size q=2, ambient dimension exactly
twice the Sidon-space dimension) — every other regime provably loses a constant factor, an
elementary reduction we didn't re-derive in full but is straightforward algebra. The problem: a
cited theorem (Castello et al.) gives an exact norm criterion showing the standard explicit
construction family (Roth–Raviv–Tamo's monomial graphs) is <em>completely empty</em> in that exact
regime, for every dimension — not a weak construction, a real nonexistence result for the whole
family. So the two explicit 5-dimensional cores found here are real, but nothing in the known
toolkit can grow them into the unbounded critical spaces a density-one answer needs. Exhaustive
finite searches (not independently reproduced by us) found zero completions of either core at the
next critical dimension, and zero binary critical Sidon spaces at all for dimension 5 — extending a
previously published dimension-4 nonexistence result.</p>

<p><strong>The honest state of play, in the source's own labeling (which we're not overriding):</strong>
the explicit constructions and the checked citations are solid; whether unbounded binary critical
Sidon spaces containing these specific cores exist at all is explicitly marked open, not conjectured
either way with confidence — a real, sharper reformulation of where #44's next real test sits, not a
new dead end.</p>

<hr>

<p><strong>Round 5, same day: a parallel question — does going to a cubic extension field restore
the near-universal coverage rate quadratic Bose–Chowla lost at size five? No, cleanly.</strong> Round
2 found quadratic (F<sub>q²</sub>) Bose–Chowla hits 1,030/1,035 size-4 patterns. Round 3 found it
drops hard at size 5. The natural next question: does moving to a cubic extension (F<sub>q³</sub>)
recover a high hit rate for size-5 patterns, the way going up a degree seemed like it might help? An
agentic run (Codex, GPT-5.6 Sol, max reasoning effort) tested this directly on a fixed sample of 20
size-5 Sidon sets, and the answer is a clean, structural no.</p>

<p><strong>Why, exactly.</strong> The obvious generalization — take one level of a linear functional
on F<sub>q³</sub> — isn't even Sidon (a level has q² elements, provably too many for the group of
order q³−1). The one construction that IS genuinely Sidon and near-optimal at cubic degree turns out
to just be the classical Singer difference set in disguise, with only two essential parameters after
accounting for scalar redundancy — not three, so a 5-point pattern (3 real conditions) is still
generically overdetermined, same problem as before. A third variant (a "norm-one functional level")
does get the hoped-for three-parameter recurrence, but Sidonicity stops being automatic — an
exhaustive search over every parameter at every prime q≤199 found zero certificates from it.</p>

<p><strong>We independently rebuilt both positive certificates from scratch — exact match.</strong>
The quadratic search hit 6/20 of the sample; the cubic projective (Singer) search recovered only 1
more, with two explicit certificates: {0,1,10,15,18} at q=37 with cubic recurrence
z³=z²+20z+2, and {0,1,12,16,22} at q=127 with z³=3z²+99z+106. We reimplemented the finite-field
arithmetic ourselves (not the source's code): confirmed both cubics are irreducible mod q, confirmed
the root has the full multiplicative order q³−1 in each case (genuine primitivity, not just
irreducibility), and confirmed the resulting difference set's prefix matches exactly —
{0,1,10,15,18} at modulus 1407, {0,1,12,16,22} at modulus 16257, both exact.</p>

<p><strong>Verdict, in the source's own words: "strong negative structural partial."</strong> Cubic
extension doesn't create a new usable family — it either fails to be Sidon, collapses back to
Singer, or requires an extra global Sidonicity filter that empirically finds nothing. The rule "size
m becomes tractable around degree m−2" doesn't hold. Scope caveats named honestly in the source:
prime base fields only, q≤199 only, one fixed 20-set sample, not a claim about every size-5 pattern
— a real, clean negative result, not a proof of general nonexistence.</p>

<hr>

<p><strong>Round 6, next day: two reasoners, same question, working independently — and a fact
Round 4 explicitly left unverified now genuinely is.</strong> Round 4 asked whether U₀ and U** (the
two 5-dimensional "native core" binary critical Sidon spaces) extend to dimension 6, and reported
"zero binary critical Sidon spaces at all for dimension 5" — but flagged plainly that this exhaustive
claim was <em>not independently reproduced by us</em>. We fired the same follow-up brief through two
separate channels at once — Codex (agentic, GPT-5.6 Sol) and a fresh ChatGPT Pro chat — without
either seeing the other's work.</p>

<p><strong>They agree on everything checkable, and one of them actually closed the gap Round 4 left
open.</strong> Both independently reconstructed the identical field definitions for U₀ and U**,
cited the same literature (Roth–Raviv–Tamo's Sidon-space/orbit-code equivalence; Gluesing-Luerssen–
Morrison–Troha's real, published k=4 exhaustive nonexistence result, arXiv:1403.1218 — we pulled the
actual PDF and confirmed the exact passage; Castello et al.'s norm criterion, JAC 2023, confirmed
Theorem 4.5 verbatim), and reached the same overall verdict: genuinely open, no construction, no
general nonexistence proof. The Pro return went further on one specific point: it actually re-ran
the k=3/4/5 exhaustive search itself rather than inheriting Round 4's number. We independently
reproduced all three from scratch, in a fresh implementation, in seconds — k=5 alone is 33,554,432
graph-normalized candidates, of which 32,841,152 have full product span and exactly zero are Sidon,
confirmed exactly. Also hand-verified a real "full span but not Sidon" collision at k=5 (pairs
{1,21} and {2,6} both landing on the same product in the field) to make sure "zero" wasn't a search
bug.</p>

<p><strong>What's now a genuinely new, triple-verified fact.</strong> No binary critical Sidon space
exists at dimension 5 — extending the only previously <em>published</em> nonexistence point (k=4,
2014) by one dimension. This wasn't in print anywhere we could find, and it's now survived two
independent reasoners plus our own from-scratch computation. We also directly brute-forced the
narrower question Round 4 left as a proof sketch — does either specific core (U₀, U**) extend to
dimension 6 in its own native field — and confirmed zero extensions across every one of the 127 and
255 cosets respectively.</p>

<p><strong>Still open, precisely.</strong> Neither reasoner found a construction or an unbounded
nonexistence proof. Both suggest the same kind of next move (a structural classification of the
"residual injections" / field-realizable alternating-code family a completion would have to belong
to) rather than another brute-force round at a bigger bound — we're taking that steer.</p>
`,
    links: [
      { label: "erdosproblems.com/44", url: "https://www.erdosproblems.com/44" },
      { label: "Alexeev–Mixon, arXiv:2510.19804", url: "https://arxiv.org/abs/2510.19804" },
      { label: "Sawin's proof (MathOverflow)", url: "https://mathoverflow.net/questions/501983/can-every-sidon-set-of-size-3-be-extended-to-a-finite-perfect-difference-set" },
      { label: "Eberhard–Manners, arXiv:2107.05744", url: "https://arxiv.org/abs/2107.05744" },
      { label: "Roth–Raviv–Tamo, Sidon spaces, arXiv:1705.04560", url: "https://arxiv.org/abs/1705.04560" },
      { label: "Gluesing-Luerssen–Morrison–Troha, arXiv:1403.1218", url: "https://arxiv.org/abs/1403.1218" },
      { label: "Castello et al., JAC 2023 (DOI)", url: "https://doi.org/10.1007/s10801-023-01275-x" },
    ],
  },
  {
    slug: "1151-chebyshev-lagrange-limit-sets",
    problemNum: 1151,
    title: "not unflagged after all — already resolved in the comment thread since April, we're an independent third verification",
    date: "2026-07-25",
    status: "proof_claimed",
    summary:
      "For closed A ⊆ [−1,1], does some continuous f have A as the cluster " +
      "set of the Chebyshev–Lagrange interpolation sequence L_n f(x₀)? We " +
      "first shipped this as an unflagged find; it wasn't. Przemek Chojecki " +
      "posted the resolution to the erdosproblems.com comment thread on 30 " +
      "April, Nat Sothanaphan confirmed it the same day, and Allen Hart " +
      "announced a Lean formalization in early May, also confirmed. The " +
      "top-level tracker badge (OPEN, 0 claimed proofs) just hadn't caught " +
      "up — we mistook a stale badge for an unflagged result because our " +
      "first pass never loaded the actual comment thread. Our contribution " +
      "is a genuine one, just smaller than we first framed it: an " +
      "independent from-scratch Lean rebuild, on our own compute, as a " +
      "second confirmation.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/1151">erdosproblems.com/1151</a>,
top-level badge still shows OPEN, 0 claimed proofs). For closed A ⊆ [−1,1],
does there exist a continuous f such that A is exactly the set of finite
cluster values of L_n f(x₀), the Chebyshev-node Lagrange interpolation
sequence, at a fixed x₀? Erdős stated the claim without proof in 1943.</p>

<p><strong>We got this one wrong on the first pass, and we're correcting
it in place rather than quietly editing history.</strong> We originally
shipped this as "we found it sitting unflagged" — that was wrong. Reading
the actual erdosproblems.com/1151 comment thread (not just the top-level
status page) shows Przemek Chojecki, the author of the "primitive row"
decomposition resolution (Ulam.ai research note, 29 April 2026), posted
it directly to the thread on 30 April. Nat Sothanaphan confirmed it that
same day: "Congrats. Standard check found no issues." Allen Hart announced
his Lean formalization of the hard direction (Theorem 1.1(a)) on 6 May,
and Sothanaphan confirmed that too. The community had this settled almost
three months before we touched it — the top-level "0 claimed proofs"
counter just tracks a separate, unused formal-submission mechanism and
never reflected the comment-thread consensus.</p>

<p><strong>What's still real here:</strong> we didn't take any of it on
faith. We cloned Hart's repo plus Google DeepMind's
<code>formal-conjectures</code> project at the exact pinned commit, on a
fresh box we controlled, and built the whole project from source:
7,997/7,997 jobs, zero errors, zero warnings. Then we ran
<code>#print axioms</code> directly on the target theorem:</p>

<p><code>'Erdos1151Formalization.erdos1151_nonempty_fixed_point' depends on axioms: [propext, Classical.choice, Quot.sound]</code></p>

<p>No <code>sorryAx</code> anywhere in the dependency chain — just the
three standard foundational axioms every real Mathlib theorem carries.
That's the hard direction, machine-checked, reproduced independently —
just not a discovery. The empty-set direction and the "other readings of
the ambiguous statement are false" sections aren't formalized in Lean,
but we read them by hand and they're standard technique.</p>

<p><strong>What we're doing about it.</strong> Full credit belongs to
Przemek Chojecki, Nat Sothanaphan, and Allen Hart. A corrected comment —
flagging only the status-badge lag, not a new result — is staged for
Patrick to post if he thinks it's worth it. The standing lesson, now
baked into how we check every candidate: always load the actual comment
thread AND the separate proof-claims page before calling anything
unflagged, never just the top-level status badge.</p>

<hr>

<p><strong>Round 2, next day: a second, completely independent verification
method — and the one piece the first pass left as "read by hand."</strong>
We had one open question left over from the original brief: a "spillover"
gap in our own understanding of Chojecki's construction, plus the empty-set
case, which Round 1 explicitly flagged as not Lean-formalized and only
checked by hand. We asked a fresh reasoner to reconstruct the whole argument
from scratch, in prose, with its own numerical checks — deliberately a
different verification method than Round 1's Lean rebuild, not a repeat of
it.</p>

<p><strong>The nonempty-A construction, rebuilt and numerically stress-tested
independently of any Lean code.</strong> We implemented the actual
mechanism — the "primitive-row Möbius block spike" that makes a Chebyshev-
node interpolation sequence hit a prescribed value at one target row while
leaking almost nothing everywhere else — as real Python, not a proof
sketch. Built the discrete spike for n=16, R=9 and checked every one of the
144 rows by direct computation: the target row landed at exactly 1.0000000000;
every other row in range came back at machine-zero (2.7×10⁻¹⁵); leakage
outside the range tracked the predicted bound and its fine structure matched
the divisor-count function τ(u) exactly, as the theory requires. Extended
this into a genuine continuous tent function (not just the discrete atoms)
and re-checked — same clean result, small artifact only from finite tent
width. Then built the full diagonal construction for an explicit two-point
closed set, checked all 4 selected rows hit their exact targets, and sampled
~45 non-selected rows spanning n=2 to 700,000: every single one sat at the
base point to 6 decimal places except exactly the one row theory predicts
should leak (n=70,000), which leaked by exactly the predicted small, correctly-
signed amount. Zero surprises anywhere.</p>

<p><strong>The empty-set case, upgraded from "standard technique" to an
actual read of the actual paper.</strong> Round 1 handled A=∅ by hand
without citing a specific source. This round found and read the real
paper: Erdős, "Corrections to two of my papers," Annals of Mathematics (2)
44 (1943), 647–651 — a genuine erratum to his own 1941 paper (an error
found by Schönberg), which fully proves a related but distinct theorem:
for x₀ = cos(pπ/q), p,q odd, there's a continuous f with |L_n f(x₀)| → ∞.
That theorem is fully proved, not the assertion this whole problem traces
back to — the 1943 paper's own "Added in proof" paragraph is where Erdős
states the general closed-set claim WITHOUT proof, which is the actual
origin of Erdős Problem #1151. Confirmed the empty-A case here uses only
the proved theorem, never the unproved assertion — non-circular.</p>

<p><strong>Verdict: not a new solve, but real, additional, independently-
sourced verification.</strong> Two structurally different checks — Round 1's
Lean compilation and Round 2's from-scratch numerical reconstruction — now
both confirm the same result, plus a direct primary-source read closes the
one piece that was previously just "standard technique, trust us." Still
Chojecki, Sothanaphan, and Hart's result, not ours; we're a third and now
fourth independent set of eyes on it.</p>
`,
    links: [
      { label: "erdosproblems.com/1151", url: "https://www.erdosproblems.com/1151" },
      { label: "Ulam.ai paper (PDF, 29 Apr 2026)", url: "https://www.ulam.ai/research/erdos1151.pdf" },
      { label: "Allen Hart's Lean formalization (Main.lean)", url: "https://github.com/AllenGrahamHart/FormalConjectures-Bench/blob/main/formalizations/erdos1151/Erdos1151Formalization/Main.lean" },
      { label: "Erdős 1943, \"Corrections to two of my papers\" (PDF)", url: "https://www.renyi.hu/~p_erdos/1943-03.pdf" },
    ],
  },
  {
    slug: "409-totient-shift-iteration",
    problemNum: 409,
    title: "#409: how fast does n ↦ φ(n)+1 reach a prime? The constant drops from 5/4 to exactly 1",
    date: "2026-07-25",
    status: "in_progress",
    summary:
      "F(n) counts iterations of n ↦ φ(n)+1 until a prime is hit. New " +
      "elementary potential-function theorem pins the leading constant to " +
      "1 (down from 5/4) and resolves the prime-square case cleanly; with " +
      "Rosser–Schoenfeld, F(n) ≤ √n + (7/4)loglog n + O(1). Exponent below " +
      "1/2, and the general fixed-prime-basin question, stay open.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/409">erdosproblems.com/409</a>,
OPEN, 0 claimed proofs — but with real prior community engagement, Cambie
and Tao both credited on the page). Let T(m) = φ(m)+1 and F(n) the number
of iterations before hitting a prime. How good an upper bound can you get
on F(n)? Can infinitely many n reach the same fixed prime? What's the
density?</p>

<p><strong>The result.</strong> A refined potential function
H(n) = √n + {√n} − 1/2 + Σ_{p≤√n} c_p (c_p a positive per-prime correction
of order 1/p) satisfies F(n) ≤ H(n) exactly. The old obstruction — prime
squares looked like they cost a real π(√n)-sized penalty — turns out not
to be real: under H, prime squares are ordinary one-step descents, only a
harmonic-over-primes correction. Elementary consequence: F(n) ≤ √n +
(7/8)log n + 1/2. Pulling in Rosser–Schoenfeld's explicit Mertens estimate
(1962, Illinois J. Math) sharpens the log n down to loglog n. Either way,
the leading constant on the √n term is now exactly 1, down from 5/4.</p>

<p><strong>We rebuilt every checkable claim from scratch before trusting
it.</strong> Sieved φ and F(n) for all n up to 2,000,000 ourselves. The
exact theorem F(n) ≤ H(n) — zero violations through 200,000. The derived
bound F(n) ≤ √n + 1/2 — zero violations through 2,000,000, extremal
exactly where claimed (n=15, F(15)=2, ratio 2/√15). The specific 4-step
balanced-semiprime descent chain offered as evidence that lowering the
exponent below 1/2 is genuinely hard (21293=107·199 → 20989=139·151 →
20701=127·163 → 20413=137·149 → 20129, prime) — every factorization and
transition checks. The exact finite basins of the first two nontrivial
targets, B₅={5,8,10,12} and B₇={7,9,14,15,16,18,20,24,30} — exact match,
and independently cross-validated against OEIS A229487's actual recorded
values. Every citation (OEIS A039651/A039652/A229487, Leonetti–Luca
arXiv:2302.01783, Rosser–Schoenfeld 1962) is real and correctly
characterized.</p>

<p><strong>What's still open.</strong> The exponent can't be pushed below
1/2 with this method — that four-semiprime chain is exactly why, and a
real fix needs ruling out arbitrarily long globally-compatible chains,
not a better one-step estimate. The general fixed-prime-basin question
(infinitude and density for an arbitrary target prime, not just 5 and 7)
reduces to an equivalent infinite inverse-totient chain question, which
we didn't settle either way. A partial-progress comment citing all of
this is staged and ready to post.</p>
`,
    links: [
      { label: "erdosproblems.com/409", url: "https://www.erdosproblems.com/409" },
      { label: "OEIS A039651", url: "https://oeis.org/A039651" },
      { label: "OEIS A229487", url: "https://oeis.org/A229487" },
    ],
  },
  {
    slug: "477-erdos-graham",
    problemNum: 477,
    title: "Closing the Erdős–Graham conjecture — every K≥3, one construction",
    date: "2026-07-23",
    status: "proof_claimed",
    originatedByUs: true,
    summary:
      "Erdős and Graham asked in 1980 whether every set of K-th powers has a " +
      "tiling complement. We think the answer is yes for every K≥3 — which, " +
      "with the known negative case at K=2, closes the conjecture in full.",
    body: `
<p><strong>The claim.</strong> In 1980, Erdős and Graham asked: for a set B ⊆ ℕ,
does there exist A ⊆ ℤ such that every integer is <em>uniquely</em> the sum of
one element of A and one of B — a "tiling complement"? For B = the K-th powers,
K=2 (squares) was already known to fail in the literature. Whether every K≥3
works was open for 46 years. We think we closed it: yes, for every K≥3.</p>

<p><strong>How.</strong> Started narrow — just K=3 — and checked it hard
against primary sources (read Heath-Brown 2008 and Browning–Heath-Brown 2005
directly, not abstracts; re-derived the exponent balancing by hand; rebuilt
the "27 lines on a cubic surface" argument from scratch). It held. Asked
GPT-5.6 Sol to push the same construction to every K≥3 by one uniform
argument. It came back claiming the whole thing. We ran a second round
explicitly trying to break it — found one real bug (a wrong genus formula for
even K), traced it by hand, and confirmed it's arithmetically inert: the
actual bound never uses genus, so the theorem survives untouched.</p>

<p><strong>The one honest line:</strong> erdosproblems.com requires a human
proof-check or a Lean formalization before something goes up on their forum.
We hold ourselves to that same bar before we call this "posted" there — so
for now it's labeled <strong>CLOSED</strong> here and nowhere else, and we'll
update the record the moment it clears theirs too.</p>

<p><strong>Receipts:</strong> <a href="https://github.com/pw/erdos477-cubic">github.com/pw/erdos477-cubic</a>
— full writeup, full verification trail, nothing hidden.</p>
`,
    links: [
      { label: "github.com/pw/erdos477-cubic", url: "https://github.com/pw/erdos477-cubic" },
      { label: "erdosproblems.com — background", url: "https://www.erdosproblems.com" },
    ],
  },
  {
    slug: "677-lcm-bridge",
    problemNum: 677,
    title: "Does lcm(n+1, …, n+k) ever repeat later on? — k=2, k=3, k=4 all closed",
    date: "2026-07-24",
    status: "in_progress",
    summary:
      "k=2, k=3, and k=4 are fully closed, each independently verified — " +
      "k=4 cross-checked against a real 1975 paper. k=6's overlapping case " +
      "is now fully classified too (verified by independent brute force), " +
      "reduced to four explicit curves for the hard disjoint case — honestly " +
      "not yet closed, but the exact remaining computation is now specified.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/677">erdosproblems.com/677</a>).
M(n,k) = lcm(n+1, n+2, …, n+k). Does M(n,k) ever equal M(m,k) for m ≥ n+k?
Our own brute-force search this morning (k=2..11, n<4,000) found zero
collisions — a real signal, not a guess. Here's what came back.</p>

<p><strong>k=2 — closed, trivially.</strong> M(n,2) = lcm(n+1,n+2) =
(n+1)(n+2), since consecutive integers share no factors. Strictly increasing.
Never repeats, full stop. Confirmed directly.</p>

<p><strong>k=3 — fully classified.</strong> The <em>only</em> pair with
M(n,3) = M(m,3), n &lt; m, in existence is (n,m) = (2,3): lcm(3,4,5) =
lcm(4,5,6) = 60. Everything else, forever, is distinct. We didn't take the
algebra on faith — we independently brute-forced every n up to 200,000 and
found exactly that one collision and no others, which is strong empirical
confirmation the classification is complete. (Under the hood, the proof
routes through a genuine cubic unit equation in ℤ[∛2] — real algebraic number
theory we didn't re-derive by hand, but the conclusion it produces matches
our search exactly.) Note (2,3) doesn't violate the original question anyway
— it's an <em>overlapping</em> pair (m=3 &lt; n+k=5), not a counterexample to
the disjoint case actually asked.</p>

<p><strong>The boundary case, for every k.</strong> A genuinely new piece: is
M(n,k) = M(n+k,k) — the tightest possible disjoint pair — ever possible? Proven
no, for every k ≥ 2, via a clean prime-gap argument (Sylvester–Schur for large
starting points, Nagura's theorem for the rest, one finite case checked by
hand). We independently verified this holds with zero violations across
k=2..29, n up to 2,000.</p>

<p><strong>What's still open:</strong> general k with a gap bigger than the
boundary (m &gt; n+k). That's the actual remaining content of #677. One honest
process note: Erdős's original 1979 statement used the strict inequality
m &gt; n+k — our brief's inclusion of the boundary case m = n+k was an
extension beyond what he originally asked, which is exactly why proving it
impossible is a real (if narrow) addition, not just a restatement.</p>

<p><strong>Round 2 — k=4 fully closed.</strong> The only collision anywhere
is (n,m)=(1,2): lcm(2,3,4,5)=lcm(3,4,5,6)=60, again overlapping, not a
counterexample. The proof is a genuine Cohn–Kedlaya-style Pell certificate —
reduce to V²−3U²=−2, track a specific residue class of the solution
sequence through a finite congruence cover (three primes, mod 8 and mod 48),
then use quadratic reciprocity to eliminate every remaining case. This time
we didn't just check the conclusion — <strong>we ran the actual certificate
script ourselves</strong>, verifying the primality of all three primes, the
full congruence cover, and the reciprocity computation, completely
independently. Every assertion passed. We also independently re-derived the
underlying Pell algebra by hand (exact arithmetic in ℤ[√3]) and confirmed a
real classical cross-check: a 1975 paper (Ponnudurai, <em>J. London Math.
Soc.</em>) proves the broader unrestricted equation has exactly two positive
solutions — the one we found, plus one more that fails our problem's extra
congruence condition (we confirmed that failure directly too). Two
independent methods, same answer.</p>

<p><strong>A real negative result, just as valuable.</strong> We also now
know <em>why</em> the diagonal/routing framework that worked for the
boundary case can't close general k on its own — an explicit construction
(large primes placed via CRT) satisfies every transport constraint without
being a real collision. Closing all k needs a genuinely different
ingredient: a joint "consecutive-integers" realization condition on both
windows at once, not just prime-power routing.</p>

<p><strong>Where k=5 and k=6 actually stand:</strong> not equally hard. k=5
reduces to seven genus-6 curves — real, hard arithmetic geometry. k=6
reduces to just four elliptic curves — a much more tractable next target.
Counterintuitively, k=6 before k=5 is the right order.</p>

<p><strong>Round 3 — k=6 pushed hard, honestly not closed.</strong> The
overlapping case (windows that share terms) is now <em>completely</em>
classified: exactly three collisions exist anywhere, full stop —
(n,m)=(3,4), (5,6), (13,15). We didn't take that on faith — an
independent brute-force search out to n=2000 found the identical three,
nothing else. The disjoint case reduces to an integral point search on
four explicit elliptic curves, and we verified every piece of that
reduction ourselves: the valuation bookkeeping that forces the ratio
between two windows into {2, 5/2, 5, 10}, the compression identity that
turns a degree-6 product into a genuine cubic, and — the sharpest
check — a "trap" the brief itself flagged: some integer points on these
curves are real points but NOT real window pairs (they fail a
square-coordinate test). We verified two such decoy points directly,
and verified the three genuine ones map back to exactly the three known
collisions. Nothing here overclaims: the brief explicitly declined to
"dress up" a rank computation as a proof, because the four curves need a
harder, non-routine certified integral-point method (elliptic
logarithms + a Mordell–Weil sieve, not just computing ranks) — real
literature on exactly this shape of problem, confirmed to exist. k=6
stays open, but the actual remaining computation is now fully specified,
down to the code that would run it.</p>

<p><strong>The bigger payoff: what "joint realization" actually is.</strong>
The earlier negative result showed prime-routing alone can't close
general k. This round names the real replacement: a family of curves
built the same way for every k, whose genus climbs with k in a precise,
checkable pattern — a conic for k=4, an elliptic curve for k=6, genus 3
for k=8, genus 6 for k=10 (matching the seven genus-6 curves already
found for k=5). The honest diagnosis of what's actually missing: not a
congruence condition, but a uniform way to control these curves' Selmer
data across every k at once — real arithmetic geometry, not a
shortcut waiting to be found.</p>
`,
    links: [
      { label: "erdosproblems.com/677", url: "https://www.erdosproblems.com/677" },
      { label: "Read the round 1 ChatGPT exchange", url: "https://chatgpt.com/share/6a630fc7-6600-83e8-9554-dc57128ece79" },
      { label: "Read the round 3 exchange (k=6, honestly not closed)", url: "https://chatgpt.com/s/t_6a63faca58148191bca22c5ae3da93c5" },
    ],
  },
  {
    slug: "324-sidon-polynomial",
    problemNum: 324,
    title: "An integer polynomial with all pairwise sums distinct — narrowed hard, not closed",
    date: "2026-07-24",
    status: "in_progress",
    summary:
      "Four rounds in. Every leading coefficient u is reachable for SOME " +
      "v, but round 4 found a genuine mod-7 wall: (7,1) specifically is " +
      "unreachable by this whole construction family — real information, " +
      "not just a failed search, and we caught and dropped an " +
      "overreaching claim in the same return.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/324">erdosproblems.com/324</a>).
Does f(x) ∈ ℤ[x] exist with all pairwise sums f(a)+f(b) distinct? The trap: the
obvious candidate (f(x)=x⁵) is only conjectured to work, and that conjecture is
implied by Lander–Parkin–Selfridge — a separate, hard, famous open problem.
We flagged that explicitly in the brief and asked for something that doesn't
quietly reduce to it.</p>

<p><strong>Finding 1 — killed an entire family, unconditionally.</strong> For
<em>every</em> positive integer A, x⁵+Ax⁴ has an explicit collision. The
construction: 2⁴+17⁴−13⁴−16⁴ = −10560 and 2⁵+17⁵−13⁵−16⁵ = 20 — opposite
signs, so scaling all four indices by L = 528·A produces an exact collision.
We checked the base identity and the general formula ourselves for A = 1, 2,
3, 5, 10 — exact match every time. The striking part: for A=1 this predicts
a collision at indices (1056, 8976, 6864, 8448) — <strong>the exact same four
numbers</strong> our own from-scratch brute-force search found earlier today,
before we'd seen this formula. Two independent methods landing on the same
answer is about as good as verification gets.</p>

<p><strong>Finding 2 — why irrational works and rational can't.</strong> A
clean pinning argument: for irrational α, n⁵+αn⁴ has distinct real pair sums,
because a collision would force two independent integer conditions (both a
4th-moment and 5th-moment match) that already pin the pairs down to being
identical. A rational coefficient collapses those two conditions back into
one — which is exactly why Ruzsa's real construction needs genuine
irrationality, and why no rational polynomial can simply imitate it to
within a small enough error (a short limit argument rules that out flatly).</p>

<p><strong>Finding 3 — the Faltings shortcut doesn't work.</strong> "The
collision equation is high-degree, so genus/Faltings kills it" was our own
loose intuition going in. It's dimensionally wrong: the collision locus is a
three-dimensional hypersurface, not a curve. Faltings applies to curves.
A real geometric approach needs an extra invariant to cut that down first.</p>

<p><strong>Round 2 — how far does the construction actually reach?</strong> We
noticed the original 528-identity only produces a collision for u|528 (u the
leading x⁵ coefficient) — a strict subset of all possible coefficient
pairs, not "every rational." We asked for the real reach. What came back:
an exact dilation lemma (a base quadruple with D₅&gt;0&gt;D₄ reaches
precisely the coefficient pairs (u,v) with u|A and B|v, for A,B derived from
the quadruple) — plus <strong>two brand-new base identities</strong> outside
the 528 family: (2,14,11,13) reaches u|45, 52|v; (3,28,19,27) reaches u|5,
41|v. We independently verified both identities, both explicit collisions,
and a rational c=52/3 example built from the first — exact match every
time. Better still: two genuine <em>infinite families</em> of new
coefficient ratios, one accumulating toward 0, one diverging to infinity —
we checked both against the general construction for five values each,
all held exactly.</p>

<p><strong>The sharp remaining gap, now precise.</strong> Call the set of
achievable ratios 𝓡. The open question is whether 𝓡 contains every positive
rational. We now know 𝓡 contains 528, 45/52, 5/41, and two infinite
families — but not yet, say, the plain integer 5. One clean logical payoff:
if 𝓡 = every positive rational were proven, that wouldn't just kill more
individual polynomials — it would prove <em>no</em> rational c ever gives an
eventually-Sidon sequence, full stop (a dilation-chaining argument pushes
any single guaranteed collision arbitrarily far out). So closing this one
gap closes the whole "rational Ruzsa" question either way.</p>

<p><strong>Round 3 — from examples to a theorem.</strong> We pushed on the
smallest uncovered leading coefficient, u=7 (our own N=20,000 direct search
for 7x⁵+x⁴ had found nothing). What came back: a clean new identity —
(17,33,23,32) gives ratio 7/67 exactly, no dilation needed — proving
7x⁵+67x⁴ collides already below N=33 (17⁵-ish scale, not the tens-of-
thousands the earlier family needed). We confirmed the identity and the
explicit collision (both sides equal 368,939,364) exactly.</p>

<p>More importantly, that specific win generalized into a real theorem:
<strong>every positive integer u is reachable for at least one coprime
v</strong> — not found by luck, but constructed directly via a parametrized
family Q_t = (2t+1, 17t, 13t−1, 16t), choosing t=4u to force u into the
numerator. We verified the family's collision holds for five values of t
(1, 2, 5, 10, and 28 — the one that mechanically reaches u=7), including
matching the exact D₄, D₅ values by hand for t=28.</p>

<p><strong>What this doesn't do, stated precisely.</strong> This proves
"every u has SOME v" — not "u=7 works with v=1 specifically," which is a
genuinely harder, different question (needs the ratio to reduce all the way
to B=1). The gap is now sharp: it needs simultaneous control of numerator
AND denominator, not either alone. A natural next attempt — a simple affine
family aimed straight at forcing B=1 — was shown NOT to work, via a clean
moment/Vandermonde argument (any such family forces the whole 5th-power
difference to vanish identically, killing the construction before it
starts). That's a real dead end correctly identified, not just another
unsuccessful search.</p>

<p><strong>Sourcing honesty:</strong> the actual Ruzsa (2001) and
Dubickas–Novikas (2021) papers were only reachable as abstract/preview, not
full text — everything above is independently re-derived, not a
reconstruction of their internal proofs. Worth saying plainly rather than
implying we read papers we didn't.</p>

<p><strong>Round 4: (7,1) specifically is out of reach for this whole
family — a real mod-7 wall, not just a failed search.</strong> We asked
directly whether the round-3 construction could hit u=7 with v=1
exactly (not just "some v"). It can't, and there's a clean reason why:
write the quadruple as (2t+p, 17t, 13t, 16t) for any inward offset p —
this covers the original family, every dilation of it, and a natural
two-parameter enlargement. Modulo 7, the collision quantity reduces to
(2t+p)⁴+t⁴, and the fourth-power residues mod 7 are only {0,1,2,4} — no
two nonzero ones ever sum to 0. So the only way a multiple of 7 can
show up is if both t and p are themselves multiples of 7 — which, run
back through the same argument on the smaller quadruple t/7, p/7,
forces them to be divisible by 7 again, and again, forever. Impossible
for any actual t≥1. We verified this exactly: the mod-7 identity itself
(5,000/5,000 random cases), the residue-sum fact directly, and the
"7|D₄ forces 7|t and 7|p" claim against a real brute-force sweep — 6,420
genuine cases, zero exceptions. A second uniform dilation doesn't
rescue it either — we checked that algebraically too: it can only
inflate the denominator further, never free it back down.</p>

<p><strong>What we're NOT putting on this page.</strong> The brief also
argued, via a separate inequality, that the whole construction always
sits at "0 &lt; ratio &lt; 1," which it used to claim NO version of this
family can ever reach any positive integer ratio at all. We checked
that claim directly against the construction's own numbers — and it
doesn't hold: recomputing the actual ratio for the very quadruple that
produces u=7 gives a value around 14, not something between 0 and 1.
That's a real internal inconsistency, not just our own arithmetic
error (we checked it two ways). So we're keeping the mod-7 result,
which stands on its own and doesn't depend on that step, and dropping
the broader claim rather than repeating something we caught
contradicting itself.</p>

<p><strong>Where this leaves 𝓡.</strong> (7,1) is provably unreachable
by this entire construction family — the original quadruple, every
dilation, and the natural offset enlargement. That's real, useful
information: it means closing the "does 𝓡 = every positive rational"
question needs a genuinely different construction, not a bigger search
inside this one. It does not prove 7 is unreachable by any construction
whatsoever — the brief says so itself, and we agree that's the honest
scope.</p>
`,
    links: [
      { label: "erdosproblems.com/324", url: "https://www.erdosproblems.com/324" },
      { label: "Read the round 1 ChatGPT exchange", url: "https://chatgpt.com/share/6a630fd9-56fc-83e8-be6a-4605ea9bb0ba" },
      { label: "Read the round 3 ChatGPT exchange (u=7)", url: "https://chatgpt.com/s/t_6a634a66930c81918f25744a97d39e98" },
      { label: "Read the round 4 ChatGPT exchange (the mod-7 wall)", url: "https://chatgpt.com/s/t_6a63edd692a08191a833e5d045024a44" },
    ],
  },
  {
    slug: "389-shift-lemma-refuted",
    problemNum: 389,
    title: "We were wrong about #389 — and the refutation handed us something better",
    date: "2026-07-24",
    status: "in_progress",
    summary:
      "Erdős #389 itself stays open. Our shift conjecture got refuted by an exact " +
      "counterexample — then a same-day follow-up proved an exact obstruction " +
      "formula and certified a 14th minimal witness (n=28), piggybacking on a " +
      "public exhaustive computation for a different Erdős problem.",
    body: `
<p><strong>The setup.</strong> Erdős #389 asks whether, for every n, some k
makes n(n+1)···(n+k−1) divide (n+k)···(n+2k−1). Nobody knows. Bhavik Mehta's
OEIS data (A375071) gives the minimal such k for n up to 27, and staring at
those numbers we noticed a pattern: every even n's minimal witness seemed to
"shift" cleanly to a witness at n+1 (drop the smallest term, drop the
largest, shrink k by one). Ten out of eleven cases matched exactly. We sent
it to Pro as a conjecture to prove.</p>

<p><strong>It's false.</strong> Exact counterexample: (n,k) = (4, 987) is a
real witness — but the shifted pair (5, 986) is not. We didn't take that on
faith. We rebuilt both products directly from scratch (990-term and 986-term
integer products, no shared code with the brief) and confirmed it byte for
byte. There's real prior art here too: M. Ulas's 2013 paper on exactly this
problem (<em>Int. J. Number Theory</em> 9(3), with an appendix by Andrzej
Schinzel) already studied these adjacent solution sets — we couldn't get past
the paywall to check the exact table ourselves, so credit that specific
detail to Pro's read, not our own verification.</p>

<p><strong>What survived the wreckage.</strong> A clean valuation criterion —
the shift's validity reduces to one binomial-coefficient divisibility test —
and a real theorem: for even n, the shift can only fail because of a prime
p ≤ n−1. We checked this ourselves against every one of the 13 known even
minimal witnesses through n=26. <strong>Zero violations.</strong> A weaker
conjecture survives too (the minimal witness specifically always shifts) —
true in every case we can check, unproven in general.</p>

<p><strong>What this isn't:</strong> a solution to #389. The general question
is still open, and someone (SharkyKesa, on the erdosproblems.com forum) is
actively working the real thing right now. We're not claiming to have moved
that needle today — just that getting refuted cleanly, and rebuilding
something real from it, is exactly what a day without a proof is supposed to
look like here.</p>

<p><strong>Update, same day.</strong> A follow-up brief came back with real
progress — still not a proof, but the obstruction is now exact and the
verified range moved. Pro derived an identity: for a dangerous endpoint
prime p, the shifted valuation equals a p-adically-rescaled copy of the
source's valuation, minus a fixed "parity debt" Z<sub>p</sub>. We didn't
take that on faith — we stress-tested it against ~3,900 randomly generated
(m, N, p) triples in its stated domain (even n) with a from-scratch
Legendre's-formula implementation, zero exceptions, and it reproduced every
worked example in the brief exactly, including the tight n=18 case where the
shift survives with literally zero valuation to spare.</p>

<p>The verified-witness range grew too. n=28's minimal witness — k =
18,253,129,921,815 — is now certified, not just a valid upper bound. The
trick: it piggybacks on a public exhaustive computational certificate for a
<em>different</em> Erdős problem, #396 (Justin Dehorty's project), which
already proved 18,253,129,921,842 is the smallest N with a valid source at
this size. We went and read that certificate ourselves against the live
repo — the exact partition boundary and the "15 false alarms, 0 real
witnesses below it" report are really there, not just described to us. That
extends the shift conjecture's verified range from 13 minimal even witnesses
(n≤26) to 14 (n≤28), still zero violations. Two more candidates (n=30, n=32)
are named as valid shifts but not yet proven minimal — we confirmed their
arithmetic too, exactly as reported.</p>

<p><strong>What's still missing</strong> is the actual proof mechanism. The
obstruction formula shows precisely what a general argument would need —
that minimality always forces the p-adic debt to get paid — and shows why
the obvious approach ("minimal witnesses have spare slack") is false: the
n=18 case pays its debt with nothing left over. Pro's own honest lean is
mild skepticism a universal theorem exists at all.</p>

<p><strong>Update: what n=30 actually needs.</strong> No public K=14
certificate exists yet to piggyback on the way n=28 did — Dehorty's
certified results still stop at K=13, even though OEIS has now separately
published the raw K=14 and K=15 witness values (we checked the actual OEIS
data file ourselves; both numbers are really there). But the picture isn't
"go compute for months" either. A real #389-specific shortcut: for large
primes, the source condition collapses to checking only 15 numbers —
N, N−1, ..., N−14 — against a simple carry-counting rule, not the full
29-term window. We verified that reduction exactly, over 3,000+ generated
cases, zero exceptions — including a genuinely subtle exception the brief
caught on its own: the prime 29 gets a one-unit "free pass" that a naive
reuse of #396's screen would wrongly disallow. Combined with a proposed
integer-only (no floating point) sieve with a proven no-false-negative
margin, the honest compute estimate for actually certifying n=30 drops
from roughly 100,000–300,000 core-hours (porting #396's exact validator
as-is) to roughly 1,000–10,000 (a purpose-built #389 sieve) — a real,
order-of-magnitude difference, not just optimism. Still not free, still
not done. N=359,503,904,702,190 remains a verified witness, not yet a
certified minimum.</p>
`,
    links: [
      { label: "erdosproblems.com/389", url: "https://www.erdosproblems.com/389" },
      { label: "Read the actual ChatGPT exchange (the write-up)", url: "https://chatgpt.com/share/6a630faa-a284-83e8-98d6-789065972ad2" },
      { label: "Read the earlier research trace", url: "https://chatgpt.com/share/6a630fb9-b83c-83e8-945a-188cd3499f66" },
      { label: "Read the follow-up (n=28 certified via #396)", url: "https://chatgpt.com/s/t_6a63c82f2f0c8191ab5915be2a22d1ad" },
      { label: "Dehorty's #396 K=13 certificate (public repo)", url: "https://github.com/jdehorty/erdos396/blob/main/certificates/README.md" },
      { label: "Read the n=30 cost/shortcut analysis", url: "https://chatgpt.com/s/t_6a63d6a3e9948191ab513521e96ac702" },
    ],
  },
  {
    slug: "1109-squarefree-sumset",
    problemNum: 1109,
    title: "#1109: exact squarefree-sumset frontier through 2,000",
    date: "2026-08-11",
    status: "partial",
    originatedByUs: true,
    summary:
      "The asymptotic problem remains open. A second exact computation adds " +
      "ten transition indices after 1500 and proves f(N) exactly through " +
      "N=2000. A custom verifier and official PMC agree on all 201 new " +
      "eligible last-vertex decisions.",
    body: `
<p><strong>Exact finite update through 2,000 (11 August).</strong> Let f(N) be the largest
size of A &subseteq; {1,...,N} for which every sum in A+A, including each
diagonal sum 2a, is squarefree. After our earlier computation through 1,500,
the next ten transitions are</p>

<p style="text-align:center"><strong>
f(1509)=45, &nbsp; f(1535)=46, &nbsp; f(1595)=47,<br>
f(1707)=48, &nbsp; f(1735)=49, &nbsp; f(1779)=50,<br>
f(1835)=51, &nbsp; f(1919)=52, &nbsp; f(1991)=53,<br>
and &nbsp; f(1999)=54.
</strong></p>

<p>Thus f(N)=44 on 1407&ndash;1508; then it is 45, 46, 47, 48, 49, 50,
51, and 52 on 1509&ndash;1534, 1535&ndash;1594, 1595&ndash;1706,
1707&ndash;1734, 1735&ndash;1778, 1779&ndash;1834, 1835&ndash;1918,
and 1919&ndash;1990. Finally f(1991)=&middot;&middot;&middot;=f(1998)=53 and
f(1999)=f(2000)=54. Together with the earlier five transitions at 1255,
1277, 1293, 1335, and 1407, this supplies fifteen terms beyond OEIS A392165's
published endpoint at 1103 as checked on 11 August 2026.</p>

<p><strong>Why the computation is exact.</strong> Use a graph whose vertices
are the a&le;N with 2a squarefree and whose edges join distinct a,b when
a+b is squarefree. Then f(N) is exactly its clique number. When a new
eligible vertex N is added, the optimum rises from r to r+1 exactly when
its old-neighbor graph contains an r-clique. Checking that decision for
every eligible N proves every prefix by induction; ineligible N leave the
graph unchanged.</p>

<p>The primary C++ verifier recomputed every prefix from 1 through 2,000. It
visited 2,432,586,214 exhaustive-search nodes in 1:58:18, reproduced all
published and previously certified transitions, and checked every returned
witness over all diagonal and off-diagonal sums. Official PMC, built from a
pinned upstream commit, independently decided every one of the 201 eligible
last-vertex graphs from 1501 through 2000. Its complete decision digest and
all ten transitions agree exactly with the primary run. Hostile checks also
regenerated every graph, replayed 27,720 primary witness sums, tested both
solvers against brute force on small graphs, and checked selected boundaries
with CP-SAT. The frozen extension bundle includes the sources, identities,
logs, witnesses, and a fast cold reproducer.</p>

<p><strong>Scope.</strong> This is an exact finite extension only. It does not
improve Konyagin's asymptotic upper bound and does not resolve Erdős's
N<sup>o(1)</sup>, or possible polylogarithmic, conjecture. The site first
treated Problem 1109 on 24 July; that analytic attempt remains below. This
section records a later finite result, not the site's first attempt and not
a solution of the parent problem.</p>

<hr>
<p><strong>Round 1 (24 July): the analytic problem.</strong></p>

<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/1109">erdosproblems.com/1109</a>).
f(N) = the largest A ⊆ {1,...,N} with every element of A+A squarefree.
Known: log log N·(log N)² ≪ f(N) ≪ N^{11/15+o(1)} (Konyagin 2004). Erdős's
guess — f(N) ≤ N^{o(1)}, maybe even ≤ (log N)^{O(1)} — is still wide open.</p>

<p><strong>A different kind of brief this time.</strong> Everything so far on
this site (#477, #677, #324, #389) has been combinatorial number theory —
explicit integers, brute-forceable claims we could re-derive from scratch in
Python. This one is deep analytic number theory: large sieve inequalities,
Bombieri–Zannier elliptic curves, uniform point-counting bounds. We can't
brute-force our way to independent confidence here the way we could before —
worth saying that plainly rather than pretending otherwise.</p>

<p><strong>What we could verify, and did.</strong> Two load-bearing citations
— a 2025 van Doorn–Tao paper and a 2021 Naccarato theorem giving a sharper
uniform bound on rational points on elliptic curves with 2-torsion — are
both real and say what they're claimed to say (we read the actual abstracts,
not just trusted the citation). More importantly: the entire algebraic chain
from the cited input bounds to the final claimed exponent is something we
<em>could</em> fully re-derive ourselves, symbolically, from scratch — and
it matched exactly, including a general formula for how a "cluster exponent"
κ maps to a final exponent for f(N) (κ=4 gives the known 11/15, κ=3 would
give 8/11). We checked this for five values of κ independently — every one
matched.</p>

<p><strong>What we could NOT verify:</strong> whether substituting the
sharper elliptic-curve bound into Konyagin's original 2004 proof machinery
is actually legitimate at that exact step — that requires reading and
understanding Konyagin's original argument in detail (a Russian-language
1990s-2000s journal paper we couldn't fully access), which is genuinely
beyond what we can independently certify. The claim itself carries its own
honest hedge — it's presented as "a checked observation, not a priority
claim without a specialist looking it over," and we're preserving that
hedge, not upgrading it.</p>

<p><strong>The more interesting part, honestly.</strong> A real structural
argument for why <em>no</em> generic large-sieve improvement can reach
Erdős's N^{o(1)} guess — even a best-case hierarchy of increasingly refined
spacing estimates appears to converge to an exponent of 2/3, not 0. The
identified missing ingredient: a signed Fourier-phase identity (∑ S_p(t)²
= −|A|² over nonzero frequencies) that current sieve arguments discard
entirely in favor of the weaker unsigned bound. Getting past 2/3 would need
a genuinely new phase-sensitive inverse theorem, not a better sieve.</p>

<p>Not closed. Real technical content, honestly graded — high confidence on
the algebra and citations, appropriately lower confidence on the deep sieve
theory itself.</p>
`,
    links: [
      { label: "erdosproblems.com/1109", url: "https://www.erdosproblems.com/1109" },
      { label: "Exact frontier through 2,000: report, source, logs, and audit", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1109/frontier-2000" },
      { label: "Earlier frontier through 1,500", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/1109/frontier-1500" },
      { label: "OEIS A392165", url: "https://oeis.org/A392165" },
    ],
  },
  {
    slug: "700-gcd-binomial",
    problemNum: 700,
    title: "How small can gcd(n, C(n,k)) get? — one of three sub-questions may be unconditionally settled",
    date: "2026-07-24",
    status: "in_progress",
    summary:
      "A real theorem for close prime triples, plus Maynard's sieve theorem, " +
      "appears to unconditionally answer 'yes, infinitely many' to one of the " +
      "page's three sub-questions. We verified everything we could — 650 " +
      "sampled cases, zero disagreements — but this needs outside eyes before " +
      "we call it settled.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/700">erdosproblems.com/700</a>).
f(n) = min over 1&lt;k≤n/2 of gcd(n, C(n,k)). Three sub-questions: (a)
characterize composite n with f(n)=n/P(n); (b) are there infinitely many
composite n with f(n) &gt; √n; (c) is f(n) ≪_A n/(log n)^A for every
composite n?</p>

<p><strong>A real correction first.</strong> The P(n) in the 1978 source
paper is the largest PRIME-POWER factor (write Q(n) for it), not the
largest prime factor P⁺(n) — a distinction our own earlier data mixed up.
Only Q(n) makes the "easy bound" f(n) ≤ n/log n actually work.</p>

<p><strong>The claim: question (b) has an unconditional proof.</strong> For
prime triples p&lt;q&lt;r with q=p+a, r=p+a+c, and D=a+c, if p is large
enough relative to D (specifically p &gt; 10D²), the answer to f(pqr) is
exactly one of two values depending only on whether the gaps are increasing
(c&gt;a) or not: f(pqr)=pq if c&gt;a, or f(pqr)=p if c≤a. Combined with
Maynard's theorem (2013) — which guarantees infinitely many translates of a
suitable "admissible" prime-tuple pattern containing at least 3 primes at
once — a specific superincreasing construction produces infinitely many
prime triples with strictly increasing gaps, satisfying the size condition,
giving f(pqr)=pq &gt; √(pqr) for all of them.</p>

<p><strong>What we verified ourselves, independently.</strong> The core
identity underlying the whole argument (checked exactly for all n&lt;60).
Both concrete worked examples: (461,463,467) → f=213,443=461×463 exactly;
(457,461,463) → f=457 exactly. The n=78 counter-check (confirms the size
condition p&gt;10D² is load-bearing — 78=2·3·13 has increasing gaps but
fails the theorem's own hypothesis, and indeed f(78)=2, not the "increasing
gaps" prediction). Then the big one: we generated the actual qualifying set
of prime triples (p&lt;q&lt;r&lt;20,000, p&gt;10(r−p)²) ourselves — got
8,257 triples against a claimed 7,576 (a real, unexplained discrepancy we're
flagging, not papering over) — and sampled 650 of them at random, computing
f(pqr) exactly via Kummer's carry-counting theorem (fast even though n=pqr
can exceed 10¹²). <strong>Zero disagreements with the theorem's prediction
across all 650.</strong> We also confirmed Maynard's 2013 paper is real and
says what's cited.</p>

<p><strong>Why we're not calling this "closed."</strong> Pro's own words:
"the sensible next step is an independent line-by-line audit... the part I
have not established is whether this argument already exists somewhere in
the literature." We take that seriously. Statistical sampling — even 650
clean cases — is not the same as verifying the actual Lucas-digit-condition
proof line by line, and we have not personally checked whether this
specific close-prime-triple result already sits in the literature on
"digit conditions in binomial coefficients," a well-studied area. Given how
much confirms cleanly, we think this is very likely real — but a genuinely
new answer to a named sub-question of an open Erdős problem is exactly the
kind of claim that deserves outside eyes before anyone treats it as settled.</p>

<p><strong>Sub-questions (a) and (c):</strong> (a) gets an exact but
algorithmic characterization for close prime triples, not a full
classification. (c) — the general analytic bound — is explicitly not
advanced by this argument at all.</p>
`,
    links: [
      { label: "erdosproblems.com/700", url: "https://www.erdosproblems.com/700" },
    ],
  },
  {
    slug: "1108-factorial-powers-brocard",
    problemNum: 1108,
    title: "#1108 turns out to be Brocard's 150-year-old equation wearing a disguise",
    date: "2026-07-24",
    status: "in_progress",
    summary:
      "Do sums of distinct factorials contain only finitely many perfect " +
      "powers? The two-term case collapses exactly onto Brocard's equation " +
      "— open since 1876. No proof, but a real quantitative bound, a fully " +
      "reproduced computational sweep, and a concrete new angle on Brocard " +
      "itself.",
    body: `
<p><strong>The question</strong> (<a href="https://www.erdosproblems.com/1108">erdosproblems.com/1108</a>,
Erdős, Oberwolfach 1988). Let A = sums of distinct factorials. For k≥2, does
A contain only finitely many perfect k-th powers? More generally, only
finitely many "powerful" numbers (every prime factor with exponent ≥2)?
Nobody knows — not even the two-term case.</p>

<p><strong>The reduction.</strong> Erdős and Obláth proved in 1937 that
n!+m!=x^p has only finitely many solutions across every exponent p, with one
boundary case they couldn't close: x^k−1=n!. Pollack and Shapiro later
killed k=4 there too. That leaves exactly k=2 open: Brocard's equation,
1+n!=y², unsolved since 1876. So the entire two-term version of #1108
collapses onto one question that already has a name and a century and a
half of failed attacks behind it. We checked both citations directly —
real papers, saying what they're claimed to say.</p>

<p><strong>A real quantitative bound.</strong> A clean lemma: if
n₁!+...+n_r!=x^k with n₁ the smallest chosen index, every small prime
p≤n₁ forces a minimum leftover valuation in the quotient — call the product
of those forced factors C_k(n₁). We stress-tested the lemma ourselves (500
randomly constructed cases, zero exceptions), then used it to derive: the
gap between the largest and smallest chosen index grows at least like
n₁/log(n₁), with an exact constant (ln 2 for squares — we checked the
constant numerically to 6 decimal places). That's twice what "powerful"
alone forces. It also implies the number of terms r must itself grow like
log(n₁)/loglog(n₁) as n₁ grows — a counterexample can't just add one term
and coast. We could not independently re-derive this last bound's own
machinery (it leans on Brindza–Erdős's actual 1991 short-interval-prime
argument) — flagging that honestly, same as we did on #1109 earlier
today.</p>

<p><strong>The computational sweep, fully reproduced.</strong> We enumerated
all 1,048,575 nonempty subsets of {1!,...,20!} ourselves, from scratch, no
shared code. Eighteen perfect powers exist in that range — we found the
identical eighteen, exact roots and exponents, down to the largest:
1,183,893² = 1!+2!+3!+7!+8!+...+15!. Seven more numbers are powerful
without being a perfect power — we found the identical seven. Complete
match, not a sample.</p>

<p><strong>A live next target, not a proof.</strong> Wilson's theorem gives
a genuinely concrete new angle on Brocard specifically: for a prime q=n+s,
n! is forced to a specific residue mod q, turning "1+n! is a square" into a
quadratic-character condition you can actually test. We verified the
underlying congruence exactly (1,624 cases, zero exceptions) and the
resulting ruling-out rule — 2 is a nonresidue mod q when q≡3 or 5 (mod 8),
666 cases, zero exceptions. Not a proof. A specific, checkable question
("does every large n have a small shift s where this character condition
kills it") that's more concrete than where Brocard's equation stood this
morning.</p>

<p><strong>Update: we were half right, and we should have found this
sooner.</strong> The exact Wilson identity we "discovered" is Lemma 1.1 of
a real 2008 paper — Helou & Haddad, <em>Ramanujan Journal</em> 17 — right
down to the D₂=2, D₃=2 example. We're crediting it plainly, not presenting
it as new. What's genuinely new is the question we asked next: does every
large n get ruled out by a SMALL shift s? <strong>The answer is no, and
not just "hard" — provably false.</strong> For any fixed bound S on the
shift, the fraction of n it can possibly cover goes to zero (there simply
aren't enough primes n+s in a fixed-width window relative to how many n
there are) — and there's an explicit, elementary reason it must miss
infinitely many n outright: take n to be a multiple of lcm(2,...,S), and
every n+s for 2≤s≤S is divisible by s, hence composite, hence not even a
candidate. We checked this exactly, for S up to 20, by hand. Worse: even
letting the shift grow like log(n) can't work, because known maximal
prime-gap results (Baker–Harman–Pintz onward) guarantee gaps that
outpace any fixed multiple of log(n) infinitely often — a real citation,
not a guess.</p>

<p><strong>What actually survived: a sharper, still-open conjecture.</strong>
We ran an exact sweep, n up to 10,000,000, testing shifts up to 500 —
independently reproduced from scratch, and it matches on every number we
checked: the only n with no witness anywhere in that range are
<strong>4, 5, and 7</strong> — which aren't holdouts, they're the three
actual known solutions to Brocard's equation (1+4!=5², 1+5!=11²,
1+7!=71², since a genuine square has no nonresidue witness, ever). Every
other n up to ten million gets ruled out by some shift ≤405. The growth
of the worst-case shift tracks (log n)² remarkably cleanly — we
reproduced the exact same numbers independently: 88, 135, 215, 308 at
n=10³,10⁴,10⁵,10⁶, matching to the integer. That gives a real, precise,
still-unproven target: T(n) ≤ C·(log n)² for every n except 4, 5, 7. Not
resolved. But now it's a specific quantitative conjecture with real data
behind it, not a vague hope.</p>

<p><strong>The honest reason nothing currently closes it:</strong> the
varying shifts aren't independent tests — they're all reading the same
one character (attached to 1+n! itself). If 1+n! actually is a perfect
square, that character is principal everywhere, and every theorem about
"forcing a nonresidue" (GRH-conditional or not) explicitly assumes a
NONPRINCIPAL character to start. So "prove a nonresidue always
eventually appears" already assumes what Brocard's equation is asking.
That circularity, not a missing technique, is the real wall.</p>

<p><strong>Update: we asked the literature directly, and it answered
cleanly.</strong> Is T(n) — the least-shift hitting-time function itself
— already studied, and does a very recent (July 16, 2026) pair-correlation
paper on least quadratic nonresidues close the gap? Real answer, both
parts checked against the actual papers: the underlying witness is
classical (Helou–Haddad again), but <strong>T(n) and its (log n)²
extreme-value question appear to be genuinely new</strong> — nobody
found. The July paper (Kandhil–Languasco–Moree, confirmed real) turns
out to be a red herring, and for a precise reason: it proves a small
nonresidue exists <em>for one fixed character</em>; we need our specific,
already-prescribed number to happen to be a nonresidue at each shift —
the theorem is free to pick whichever witness is convenient, and ours
isn't. Splitting the composite discriminant into prime factors doesn't
rescue it either — the large factors are exactly the ones with no small
structure, and quadratic characters don't split additively. No standard
named conjecture (GRH, Montgomery pair correlation, Chowla–Elliott,
fixed-size Hardy–Littlewood) implies the bound — confirmed genuinely
bespoke, not just under-searched.</p>

<p>What does fall out cleanly: a real heuristic derivation. Model each
shift as an independent coin flip (prime with probability ~1/log n,
nonresidue with probability ~1/2) and the math gives
E(X,H)≈X·exp(−H/(2 log X)) — solving for where that hits 1 gives
H≈2(log X)², exactly the scale we found empirically. We checked the
algebra and the numeric table (259.8, 339.3, 429.5, 763.5, 1192.9 at
X=10⁷ through 10¹⁵) both exactly. The honest caveat, backed by a real
2026 paper on exactly this failure mode: naive independence can break
down precisely in this kind of extreme, growing-window regime, so the
leading constant (is it 2? something else?) isn't yet trustworthy even
though the (log n)² shape is. A sharper proposed test for next time:
not a bigger table of maxima, but a survival-curve slope check across
millions of values at once — a much stronger diagnostic than chasing
one more record.</p>
`,
    links: [
      { label: "erdosproblems.com/1108", url: "https://www.erdosproblems.com/1108" },
      { label: "Read the actual ChatGPT exchange", url: "https://chatgpt.com/s/t_6a63bf0eafb8819188ba8759a9fe16fa" },
      { label: "Read the literature-scoping follow-up", url: "https://chatgpt.com/s/t_6a63f4242d6881919fe6494e925c41e0" },
      { label: "Helou & Haddad 2008 (the identity's real source)", url: "https://link.springer.com/article/10.1007/s11139-008-9139-8" },
    ],
  },
  {
    slug: "931-same-prime-support",
    problemNum: 931,
    title: "#931: two blocks of consecutive integers, same set of prime factors — sporadic or infinite?",
    date: "2026-07-24",
    status: "in_progress",
    summary:
      "Do two disjoint blocks of consecutive integers with identical prime " +
      "support only collide finitely often? A real structural transfer from " +
      "our #677/#389 work, a sharper (partly-verified) counting bound, and a " +
      "computational sweep we reproduced exactly — 16 for 16.",
    body: `
<p><strong>The question</strong> (<a href="https://www.erdosproblems.com/931">erdosproblems.com/931</a>).
Fix k₁≥k₂≥3. Are there only finitely many disjoint pairs of blocks — k₁
consecutive integers starting at n₁+1, k₂ consecutive integers starting at
n₂+1 — whose products have exactly the same set of prime factors? The raw
statement is already false as stated (AlphaProof found 10! and 14·15·16,
both with prime support {2,3,5,7}) — the real question, which Erdős himself
was unsure of, is whether the exception set is <em>finite</em>.</p>

<p><strong>What transfers from #677 and #389, and what breaks.</strong> The
same offset-routing geometry from our earlier work this session survives
perfectly: every large prime in a shared support labels a unique diagonal
t=j−i in the two blocks' offset grid. We verified this exactly — on real
collisions we found ourselves, not toy cases — the routing congruence, the
per-diagonal divisibility, and the full product identity all held with zero
exceptions. What breaks is the VALUATION information that made #389 and
#677 tractable: there, a prime's exponent in one block had to relate to its
exponent in the other. Here, once both exponents are just ≥1, anything
goes. That's the entire obstruction in one line: the routing survives,
the magnitude control disappears.</p>

<p><strong>A real reduction for fixed gaps.</strong> For any fixed
(k₁,k₂,gap), every relevant prime is confined to one finite set by
construction — which makes both numbers in a block S-smooth for a fixed
finite S, and Størmer's classical S-unit finiteness theorem closes it
immediately. So finiteness is already known whenever the gap between the
two blocks is held fixed. The open content is entirely about what happens
as that gap grows — a real, if partial, structural clarification of the
question.</p>

<p><strong>A sharper counting bound — partly ours to trust, partly not.</strong>
A real 2025 preprint (Lebowitz-Lockard, confirmed live on arXiv, matches
the problem exactly) bounds the count of collisions below x by
x·exp((s log2+o(1))·loglogx/logx). The brief derives a materially sharper
x·(logx)^{s+1} via a Pell-equation reduction plus a standard mean-value
bound (Nair–Tenenbaum/Henriot). We could not independently re-derive that
machinery — same honest limit as #1109's sieve theory earlier today — and
the brief itself asks for another analytic number theorist to audit it
before any novelty claim. We're preserving that hedge, not upgrading it.</p>

<p><strong>The computational sweep — this part we reproduced exactly.</strong>
For the cleanest case (three consecutive integers vs. three consecutive
integers), we independently searched for equal-support collisions from
scratch, no shared code, up to 3,000,000 — twenty times past the reported
range where all such collisions are known to live. <strong>We found exactly
16</strong>, the same 16, including the exact starting positions of the
largest known pair (2650 and 58563) and the smallest (169 and 323). Nothing
new turned up in the 3,000,000 we checked beyond where they stopped
looking closely. We also hand-verified three of the specific named examples
digit by digit — 169·170·171 vs. 323·324·325, the length-7-vs-3 pair at
172 and 893024, and Tijdeman's own original 19–22 vs. 54–57 — every
factorization and every shared prime support checked out exact.</p>

<p><strong>Where it lands.</strong> No proof of finiteness, no infinite
family. Erdős's own proposed extra condition (n₂ &gt; 2(n₁+k₁)) turns out to
be false as a strict necessary condition — 56 of the 288 found tuples
violate it — but remains fully consistent with finiteness as a heuristic.
The honest read, and it's Pro's own: evidence leans sporadic (fixed-gap
finiteness, a stable catalog, no visible parametric family generating new
examples) but a "computational desert" is not a proof, and the observed
gaps between successive examples (622, 4093, 10932, 58562, 113397, 893023)
are exactly the kind of sequence where that matters.</p>
`,
    links: [
      { label: "erdosproblems.com/931", url: "https://www.erdosproblems.com/931" },
      { label: "Read the actual ChatGPT exchange", url: "https://chatgpt.com/s/t_6a63ce8a00b48191a4ac495a395604a1" },
    ],
  },
  {
    slug: "357-half-the-runs",
    problemNum: 357,
    title: "#357: how many strictly increasing numbers can you pick with every run-sum distinct? A clean new ceiling.",
    date: "2026-07-24",
    status: "in_progress",
    summary:
      "f(n) counts the biggest strictly-increasing sequence up to n where " +
      "every contiguous run sums to something different. New result: " +
      "f(n) ≤ n/2 + √n + O(1) — and we didn't just check the final number, " +
      "we replayed the entire proof by hand and it never once broke.",
    body: `
<p><strong>The question</strong> (<a href="https://www.erdosproblems.com/357">erdosproblems.com/357</a>,
Erdős and Harzheim). Pick 1≤a₁&lt;a₂&lt;...&lt;a_k≤n so that every "run
sum" — every sum of a contiguous stretch a_u+...+a_v — comes out different.
f(n) is the biggest k you can get. Is f(n)=o(n)? The best known lower bound
was (2+o(1))√n; nobody had a matching upper bound better than the trivial
n.</p>

<p><strong>The new result.</strong> f(n) ≤ ⌈n/2⌉ + a term that's O(√n) —
concretely, limsup f(n)/n ≤ 1/2. Not a solution to the o(n) question, but
the first real ceiling: at most half the trivial range, provably. The
argument is short enough to state in full. Take the prefix sums P₀=0,
P₁=a₁, P₂=a₁+a₂, etc. Only about √n of the early indices can stay below
n/2 (since a strictly increasing sequence of positive integers grows at
least linearly, so hitting n/2 doesn't take long). For every later index i,
walk backward from a_i until the running sum first crosses n/2 — call that
crossing sum s_i. Monotonicity is what makes this work: the term that
triggers the crossing is never bigger than a_i itself, which caps s_i at
n. Every one of those crossing-intervals ends at a different i, so — by
the problem's own hypothesis — every s_i is different too. But they're all
squeezed into the n/2 integers between n/2 and n. That's the whole
bottleneck.</p>

<p><strong>We didn't just check the arithmetic — we replayed the proof.</strong>
This one is fully self-contained, no external machinery to trust, so we
held it to a higher bar than a numeric spot-check: for real sequences we
built ourselves, we mechanically re-executed every step — computed the same
prefix sums, found the same crossing index for every i, and checked, by
hand, in code, that every single claimed property held: the early-index
count stayed under the predicted √n cap, every crossing sum landed in
[n/2, n], the "trigger term never exceeds the endpoint" monotonicity claim
never once failed, and every crossing sum really was distinct. Zero
exceptions. Then, separately, we brute-forced the TRUE maximum k by
exhaustive search (not just our own constructions) for every n from 5 to
25 — the real f(n) never once came close to violating the bound.</p>

<p><strong>What it doesn't touch.</strong> This method caps sequences that
spread evenly across [1,n] — but a sequence piled up mostly in the top half
would produce only singleton run-sums there, and this particular argument
wouldn't see anything wrong with that. Getting to o(n) needs a genuinely
different idea: collisions between sums that land <em>above</em> n, not
just inside it. The brief's own honest framing, which we think is right:
this recasts a famous hard question into a narrower, more specific one —
does a near-complete packing of the top half force a second collision
somewhere past n?</p>
`,
    links: [
      { label: "erdosproblems.com/357", url: "https://www.erdosproblems.com/357" },
      { label: "Read the actual ChatGPT exchange", url: "https://chatgpt.com/s/t_6a63d04c714481918820e610be775516" },
    ],
  },
  {
    slug: "1063-one-large-prime",
    problemNum: 1063,
    title: "#1063: a real upper-bound jump on n_k — corrected after a reader caught us overclaiming it",
    date: "2026-07-25",
    status: "in_progress",
    summary:
      "erdosproblems.com's own statement of #1063 is just 'estimate n_k' — " +
      "open-ended, and it stays open here. What we actually proved: n_k = " +
      "exp(o(k)), a genuine improvement on Cambie's exp((1+o(1))k) bound, " +
      "which fills one specific formalized open target (a Google DeepMind " +
      "Lean placeholder). A reader correctly called out an earlier version " +
      "of this entry for reading like a full solve with no checkable proof " +
      "behind it — full corrected writeup and proof now public.",
    body: `
<p><strong>Correction, first.</strong> The version of this entry that shipped
yesterday described a different, weaker construction (removing one large
prime, bound n_k ≤ (3/2+o(1))·lcm(1,...,k−1)) under a title that read like
the Erdős problem itself had fallen. A reader on X,
<a href="https://x.com/Liam06972452" target="_blank" rel="noopener">@Liam06972452</a>,
correctly called that out on both counts: it was only ever a partial result,
and we'd posted prose, not an actual checkable proof. Fair on both. Worse,
when we went to write up a proper proof to publish, we couldn't find any
saved derivation of that specific weaker bound anywhere in our own working
files — only this stronger, fully-documented result below, computed the
same day but never shipped. We don't have a clean explanation for that gap
and aren't going to pretend we do. What follows is the real, corrected
result, independently re-verified before publishing.</p>

<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/1063">erdosproblems.com/1063</a>).
n_k is the least n≥2k such that all but one of n, n−1, ..., n−k+1 divides
C(n,k). The page's own statement of the problem is simply "estimate n_k" —
open-ended, and nothing here closes it. Cambie's known bound: n_k ≤
k·lcm(1,...,k−1) ≤ exp((1+o(1))k). A specific, formalized, narrower target
does exist and is what we're actually answering: Google DeepMind's Formal
Conjectures repo has a Lean theorem, tagged "research open," asking for any
upper bound that's little-o of Cambie's — a literal unfilled placeholder,
confirmed still open the day we worked on it.</p>

<p><strong>The result: n_k ≤ exp(C·k·log log k / log k) for an absolute
constant C</strong> — so n_k = exp(o(k)), which is substantially stronger
than the little-o improvement asked for: it pulls the exponent's whole
leading order down, not just a polynomial factor off it. This came from
Codex (GPT-5.6 Sol, agentic coding tool, highest reasoning-effort tier),
given the exact valuation-transport reformulation of the problem (write
C(n,k) = ∏(n−i)/k!; divisibility becomes a prime-by-prime demand-vs-supply
covering condition) after our scout flagged #1063 as a clean match to the
same toolkit that closed pieces of #389 and #677.</p>

<p><strong>The idea.</strong> The naive fix — demand one extra multiple of
every prime power p^a≤k, to survive any single deletion — is provably
impossible whenever p^a divides k exactly (that level can never have a
surplus, for any n). The real construction instead designates one "excused"
coordinate E≈k/(log k)³ and lets primes fail at that coordinate on purpose:
small primes get extra p-adic depth stacked there; "exceptional" large
primes get a forced p² there; "regular" large primes get centered into a
window via simultaneous Dirichlet approximation. Every non-excused
coordinate ends up covered from one of three independent directions; the
excused one is proven, not assumed, to be the sole failure.</p>

<p><strong>Independently re-verified before publishing, not just
checked once:</strong> a from-scratch checker recomputes every valuation
two independent ways (Legendre's floor formula and Kummer's carry count),
recomputes the demand/supply dictionary directly, and for moderate k builds
the actual big-integer C(n,k) and checks every remainder. Re-run fresh
across 17 values of k from 4 to 300 (5 of them new, outside the original
run) — every single one: exactly one failing coordinate, always the
predicted one, zero exceptions.</p>

<p><strong>What this doesn't do — same honest caveat as before, just
higher up now instead of buried at the end.</strong> lcm(1,...,k−1) itself
still grows like exp(k); this result doesn't touch that. Our own
computational sweep shows the TRUE minimal n_k is usually far smaller than
this guaranteed bound and behaves close to chaotically as k grows — this
fixes the growth-rate target that was asked for, not the exact value, and
Erdős's actual "estimate n_k" stays open.</p>

<p><strong>The full proof, publicly checkable this time.</strong> Same bar
as #477 — independently rebuilt, independently re-verified, zero
discrepancies, but not posted to erdosproblems.com, whose own bar is human
or Lean verification, not an AI's internal rigor. Unlike yesterday's
version, there's now an actual proof document with a runnable checker, not
just a summary.</p>
`,
    links: [
      { label: "The full proof + verification, public repo", url: "https://github.com/pw/erdos1063-upper-bound" },
      { label: "erdosproblems.com/1063", url: "https://www.erdosproblems.com/1063" },
      { label: "The open theorem placeholder (Formal Conjectures / Lean)", url: "https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/1063.lean" },
      { label: "The reader who caught it — @Liam06972452 on X", url: "https://x.com/Liam06972452/status/2081031072913949146" },
    ],
  },
  {
    slug: "156-maximal-sidon-log-factor",
    problemNum: 156,
    title: "#156: Round 5 — exact maximal-Sidon values through 136",
    date: "2026-08-11",
    status: "in_progress",
    summary:
      "Does a maximal Sidon subset of {1,...,N} exist with size O(N^(1/3))? " +
      "The asymptotic problem remains open, and Rounds 1–2 explain why the " +
      "extra log in Ruzsa's construction is structural for random lifts. " +
      "Rounds 3–5 close the next exact finite frontier: a(66)=a(67)=6, " +
      "a(n)=7 for every 68≤n≤101, and a(n)=8 for every 102≤n≤136. " +
      "Complete enumerations cover normalized Sidon sets through seven " +
      "marks, while explicit maximal sets certify every upper bound. This " +
      "extends OEIS A382397 from 65 through 136 without changing the parent " +
      "problem's " +
      "asymptotic record.",
    body: `
<p><strong>The target</strong> (<a href="https://www.erdosproblems.com/156">erdosproblems.com/156</a>,
[ESS94]). A Sidon set has no repeated pairwise sums. A greedy Sidon
set in {1,...,N}, extended until nothing more can be added, is
automatically maximal and has size ≫N^(1/3) — cheap. The question
asks whether a maximal Sidon set can be built as small as O(N^(1/3)).
Ruzsa (1998) got O((N log N)^(1/3)) — one log factor above the target,
unimproved in the literature since. HONEST DECLINE, but a genuinely
useful one: literature search confirmed the record hasn't moved, and
reconstructing Ruzsa's method (it isn't freely available in full) from
first principles and its known descendants pins down exactly why the
log is there.</p>

<p><strong>Round 5 (11 August): thirty-four more exact values.</strong> Let
a(n) be the minimum size of a maximal Sidon subset of {1,...,n}. A new
complete computation proves</p>

<p style="text-align:center"><strong>a(n)=8 for every 102≤n≤136.</strong></p>

<p>For the lower bound, translate a candidate so its first mark is zero. Any
candidate in this range then has diameter at most 135, and maximality requires
its blocked component to have length at least n. Two complete seven-mark
engines, one using unordered pair sums and one using three words of positive
differences, independently enumerate all 8,515 search tasks. They agree on
4,664,137,760 endpoint attempts, 3,188,523,904 Sidon rulers, 455,390 rulers
whose blocked component contains their hull, and a longest blocked run of only
101. Complete searches through six marks give a still smaller maximum of 67.
Thus no set of at most seven marks is maximal on an interval of any claimed
length.</p>

<p>The upper certificate is one ruler:
{0,39,47,51,52,61,67,101}. Its 36 unordered pair sums are distinct and its
blocked component is [−16,119], containing 136 consecutive integers.
Translations of this ruler give maximal eight-element Sidon sets for every
n from 102 through 136; the public checker tests every outside insertion in
all 35 domains.</p>

<p><strong>Hostile audit.</strong> A third implementation uses mutable byte
arrays, a different three-mark task decomposition, and reflection symmetry.
It recovers every seven-mark counter exactly and explicitly finds zero
hull-covering rulers of diameter 102 through 135. A separate one-tree search
reproduces every row through six marks, while a literal checker rejects all
3,885 outside insertions in the upper certificates. The full author and audit
bundles, hashes, sources, and frozen outputs are public. This advances only
the exact finite sequence; the asymptotic Problem 156 remains open.</p>

<p><strong>Round 4 (11 August): the exact sequence reaches its next
jump.</strong> A complete extension of the finite computation now proves</p>

<p style="text-align:center"><strong>a(n)=7 for every 68≤n≤101,
&nbsp; and &nbsp; a(102)=8.</strong></p>

<p>The lower bound at 102 is the load-bearing new piece. Three exact engines
enumerate every normalized set of at most six marks and diameter at most 101;
their size-six totals agree at 79,208,745 raw sets, 46,198,688 Sidon sets,
and longest blocked run 67. A fourth OpenMP engine exhausts every seven-mark
Sidon ruler of diameter at most 101: 386,623,922 Sidon rulers survive the
difference test, 455,390 cover their own hull, and the longest blocked run is
exactly 101. No seven-mark set can therefore be maximal on {1,...,102}.</p>

<p>The matching upper certificates are short. The normalized ruler
{0,24,27,35,39,41,75} blocks the full interval [−17,83], so its translations
give seven-mark maximal sets for every new n from 96 through 101. At 102 the
eight-mark set {10,33,38,42,59,69,71,89} is Sidon and rejects every one of
the 94 outside points.</p>

<p><strong>Independent audit.</strong> A separate unpruned program visited all
C(101,6)=1,267,339,920 normalized seven-mark candidates, rebuilt every
difference set at the leaf, and tested insertions directly. It recovered the
same 386,623,922 Sidon rulers and the same reported optimum, while full
ASan/UBSan runs passed for the production enumerators. The public extension
bundle freezes the proof reduction, four enumerators, direct witness replay,
logs, hashes, and hostile audit. This is still a finite computational result;
the asymptotic Problem 156 remains open.</p>

<p><strong>Round 3 (11 August): the exact finite frontier moves by thirty
places.</strong> Let a(n) be the minimum size of a maximal Sidon subset of
{1,...,n}, with unordered sums including the diagonal sums 2a. The current
OEIS A382397 table stops at n=65. We now have the exact continuation</p>

<p style="text-align:center"><strong>a(66)=a(67)=6, &nbsp; and &nbsp;
a(n)=7 for every 68≤n≤95.</strong></p>

<p>This is an exact finite result, not a solution of the asymptotic Erdős
problem. Its useful reduction is a blocking lemma. If S(A) is the old
pair-sum set of a Sidon set A, define</p>

<pre><code>B(A) = A
  union {s-a:
         s in S(A), a in A}
  union {s/2:
         s in S(A), s even}.</code></pre>

<p>For x outside A, the set A∪{x} fails to be Sidon exactly when x∈B(A):
the only new sums are x+a and 2x, and failure means one of them equals an
old sum. Thus A is maximal on an interval exactly when every unused point
of that interval is blocked.</p>

<p><strong>Why the finite search is complete.</strong> Translate a candidate so
its least mark is 0, writing R={0}∪T and L=max R. Translation preserves both
the Sidon property and blocking. If the maximal consecutive run in B(R)
containing the hull [0,L] has length h, then R has a maximal translate in an
n-point interval exactly when h≥n and L≤n−1. For every n≤95 it therefore
suffices to enumerate every normalized ruler with diameter at most 94.</p>

<p>Two exact C++ engines did that for every size at most six. One stores
positive differences in a 128-bit mask and constructs the difference form of
B(R); the other stores unordered sums in a bitset and constructs the displayed
sum form. Their central representations differ, although they deliberately
share the normalization, traversal shape, and reporting scaffolding. They
agree on every row:</p>

<p><strong>k=1:</strong> 1 raw, 1 Sidon, 1 hull-covered; best run 1.<br>
<strong>k=2:</strong> 94 raw, 94 Sidon, 2 hull-covered; best run 4.<br>
<strong>k=3:</strong> 4,371 raw, 4,324 Sidon, 8 hull-covered; best run 10.<br>
<strong>k=4:</strong> 134,044 raw, 125,504 Sidon, 76 hull-covered; best run 22.<br>
<strong>k=5:</strong> 3,049,501 raw, 2,434,706 Sidon, 1,102 hull-covered; best run 42.<br>
<strong>k=6:</strong> 54,891,018 raw, 30,594,300 Sidon, 20,166 hull-covered;
best run 67.</p>

<p>The first six-mark ruler attaining 67 is
R={0,7,19,22,28,39}, whose blocked run is [−15,51]. Hence no set of at most
six marks can be maximal on any interval of length 68 through 95. The rows of
sizes at most five similarly rule out five marks at lengths 66 and 67.</p>

<p><strong>The matching upper certificates are explicit.</strong> Translating
that extremal ruler gives the six-mark witness
{16,23,35,38,44,55} for n=67; {21,25,31,40,43,60} works for n=66. Thirty
directly checked witnesses cover every n from 66 through 95, ending with
{30,31,33,48,55,59,93} at n=95. The public bundle contains both enumerators,
all witnesses, frozen logs, the proof of the reduction, and direct
sum-by-sum and difference-by-difference checkers.</p>

<p><strong>Audit and scope.</strong> Three hostile audits rebuilt the programs,
reproduced all 54,891,018 size-six candidates under sanitizers, checked the
blocking equivalence separately, and verified every outside insertion for
all 30 witnesses. One audit added a third, unpruned enumerator which visits
all 58,079,029 normalized sets of sizes one through six and tests insertion
directly from positive differences; it matched every row. No discrepancy was
found. That Round 3 computation stopped at n=95; Round 4 above supplies the
complete extension through 102. The parent question still asks for
O(N^(1/3)); the exact sequence moved, but Ruzsa's
O((N log N)^(1/3)) asymptotic record did not.</p>

<p><strong>Where the log actually comes from.</strong> Ruzsa's
construction: embed a dense Singer-difference-set Sidon set into a
small ambient group of size M, then randomly lift it into {1,...,N}.
Average-degree counting alone only needs M≫N^(2/3) — that would give
the target O(N^(1/3)). But guaranteeing every one of the ~N points
gets covered (not just almost all of them) needs a union bound over N
events, and that union bound is exactly what forces M up by a factor
of log N — coupon-collector, not Sidon combinatorics. Ruzsa's
(N log N)^(1/3) falls out of balancing √M + N/M with that M. Nobody
has shown the log is <em>necessary</em> — only that this specific
covering method needs it.</p>

<p><strong>The real find: a verified sibling result the tracker
doesn't mention.</strong> Redman, Rose, and Walker
(<a href="https://arxiv.org/abs/2109.00292">arXiv:2109.00292</a>, SIAM
J. Discrete Math. 2022) prove the exact group-theoretic analogue in
Z₂ⁿ: a maximal Sidon set of size O((n·2ⁿ)^(1/3)) — same "log-like"
factor (n = log|G|), same construction template, explicitly adapted
from Ruzsa's method. We verified the citation directly: real paper,
real authors, matches the claimed bound exactly. They also note that
Bennett–Bohman random-greedy analysis of the analogous covering
process predicts this factor is <em>tight</em> in the group setting —
suggestive, not a proof, but it's the first piece of evidence either
direction on whether Ruzsa's log is real or just an artifact of one
particular argument.</p>

<p><strong>Round 2: the log is provably structural for random lifts —
not a sloppy union bound.</strong> Round 1 left a precise question open:
is the log <em>necessary</em>, or just an artifact of Ruzsa's union bound?
For his actual independent random-lift model, it's necessary. The upper
half is Ruzsa's: each non-Singer target survives with probability at most
e^(−c·p/M). The new half is a matching LOWER bound — the Lovász local
lemma, applied to the O(p) collision events for a fixed target, whose
dependency graph has bounded degree (exactly because the Singer set is
Sidon modulo q): the survival probability is at least e^(−C·p/M). So
Ruzsa's exponential estimate is the right ORDER; there is no hidden extra
saving waiting in the dependence. We verified the load-bearing pieces
directly — the saturation counting that sets the N^(1/3) floor, Singer
(q,p+1,1) difference sets for p=2,3,5 (every nonzero residue a unique
difference, Sidon modulo q), the local-lemma condition, and the threshold
algebra.</p>

<p><strong>The threshold is sharp, and below it the failure is total.</strong>
Let U be the number of targets a random lift leaves unblocked. McDiarmid's
bounded-differences inequality (changing one height moves U by O(p²)) gives
Pr(U=0) ≤ e^(−Ω(p)) right at the log-free scale p≈M≈N^(1/3), where the
expected number of uncovered targets is E U = Θ(N) — not a sparse cleanup
set, a positive-density SEA of them. A small Monte Carlo makes it visible
even at p=5: the unblocked-target fraction falls monotonically 0.71 → 0.00
as λ=p/M crosses log N. The iid covering threshold is λ = Θ(log N). Random
heights cannot remove the log.</p>

<p><strong>A real reduction — and why it still isn't enough randomly.</strong>
Ruzsa demands every non-Singer residue class be fully covered; that's
stronger than needed. An alteration lemma (verified counting) shows that if
the initially addable points outside the Singer classes land in only L
residue classes modulo q, the lift extends to a maximal Sidon set of size at
most (p+1) + L + 2⌊(N−1)/q⌋ — the added points anchor by class, and their
within-class offsets are forced to be distinct nonzero multiples of q or
they'd create a pair-sum collision. At the critical scale p≈M≈N^(1/3) the
target drops to achieving L=O(p): holes confined to O(p) of the q≈p²
columns, not zero holes. Materially weaker — but a random critical lift
still misses it by an order of magnitude (it would need U=O(p²) where
E U=Θ(p³), the same e^(−Ω(p)) wall).</p>

<p><strong>The door that's still open: deterministic heights.</strong> The
probability bound e^(−Ω(p)) is enormously larger than the probability
M^(−(p+1)) of any one specific height assignment, so an exponentially rare,
algebraically structured labeling could still cover everything; the
concentration estimate is nowhere near strong enough to rule it out. The
log-free problem inside Ruzsa's architecture is now precise: choose p+1
labels d_u ∈ [0,M−1] with p/M=Θ(1) so that, for all but O(p) of the q≈p²
residues ρ, the set of blocked fiber-heights H_ρ(d) — each a Θ(p)-element set
of sums d_u + d_v − d_w over Singer certificates — covers all Θ(M)=Θ(p)
relevant heights. That is an almost-perfect simultaneous covering problem,
closer to an orthogonal array or an algebraic covering code than to ordinary
probabilistic selection. Parameter tuning and stronger tail inequalities are
provably dead ends; this labeling is the right next object. (Equally open: a
completely different Sidon set whose A+A−A nearly tiles [N], or a finite-group
perfect-saturation object embedded into the integers carry-aware.)</p>

<p><strong>What's still open — sharper now.</strong> The bound itself has not
moved: still no O(N^(1/3)) maximal Sidon set, and still no lower bound past
the trivial Ω(N^(1/3)) — the universal counting obstruction remains N^(1/3),
with no evidence for a universal (log N)^(1/3) floor. But the question is no
longer "is the log real or an artifact?" For random lifts it is provably real
and structural. The live question is whether a deterministic, algebraic lift
can do what random ones provably cannot — and Round 2 turns that into a
concrete design problem rather than a vague hope. Ruled out: optimizing
Ruzsa's constants or prime, routine dependency estimates, iid heights at
p=O(N^(1/3)), sparse random cleanup, and swapping Singer for any other dense
quotient (same k³/N intensity). 28 years, one log factor — still standing,
now with a named attack vector.</p>
`,
    links: [
      { label: "Exact A382397 values through 136: proofs, enumerators, witnesses, and audits", url: "https://github.com/pw/ErdosProblemADay.com/tree/main/verification/156" },
      { label: "GPT-Pro Round 2 — sharp iid threshold + alteration lemma + deterministic design (chat transcript)", url: "https://chatgpt.com/s/t_6a66d9eea8d081918708eff3fcedf56b" },
      { label: "erdosproblems.com/156", url: "https://www.erdosproblems.com/156" },
      { label: "Redman–Rose–Walker, arXiv:2109.00292", url: "https://arxiv.org/abs/2109.00292" },
    ],
  },
];

// ---------------------------------------------------------------------------
// Friends We Made Along The Way — secondary findings that aren't a numbered
// daily attempt but are real: lemmas that outlived the conjecture that spawned
// them, side quests picked up while scouting, literature we tripped over.
const friends = [
  {
    kind: "LEMMA",
    title: "The small-prime obstruction theorem",
    date: "2026-07-24",
    body: "Born from a conjecture of ours that turned out to be false (see #389). " +
      "The conjecture died; this survived: for even n, a witness-shift can only " +
      "fail because of a prime p ≤ n−1 — every larger prime is automatically " +
      "harmless. Independently verified against all 13 known minimal witnesses " +
      "through n=26, zero violations — then a same-day follow-up sharpened it " +
      "into an exact recursion formula and used it to certify a 14th witness, n=28.",
    link: { label: "See it in #389", url: "/day/389-shift-lemma-refuted" },
  },
  {
    kind: "SIDE QUEST",
    title: "Treewidth ≥6 needs at least 21 edges",
    date: "2026-07-24",
    body: "Not even an Erdős problem — a 2024 CS-theory question (Amarilli) asking " +
      "whether a graph with treewidth ≥6 could exist with ≤20 edges. Answer: no. " +
      "μ(6)=21 exactly, achieved by K₇. One citation (Joret–Wood 2018) did all the " +
      "real work; we fetched the actual paper, confirmed the theorem, and checked " +
      "the sharpness witness by hand.",
    link: null,
  },
  {
    kind: "LIT FIND",
    title: "M. Ulas already saw this coming, in 2013",
    date: "2026-07-24",
    body: "While getting refuted on #389, we found a 13-year-old paper (Ulas, " +
      "with an appendix by Schinzel, Int. J. Number Theory 9(3)) that had already " +
      "been staring at these exact adjacent solution pairs. Confirmed the paper is " +
      "real — right journal, right DOI — good reminder to check the literature " +
      "before falling in love with your own pattern.",
    link: { label: "See it in #389", url: "/day/389-shift-lemma-refuted" },
  },
];

// ---------------------------------------------------------------------------
// THE LEDGER, early internal half. Numbered problems we attempted but never
// shipped as full write-ups — briefs sent to reasoner seats and Codex waves
// that produced no publishable result. Hand-maintained. Renders on the
// homepage's unified ledger feed (ledgerRows merges this with `entries` and
// the generated `LEDGER`). If one of these ships as a full /day/ entry, just
// add it to `entries` — the homepage merge dedupes by problem number and the
// shipped row wins, so no deletion is needed here.
// Outcomes are one-line summaries of the actual run/brief writeups in
// ~/MathDyad/{briefs,runs,scout_*} — swept + reconciled 2026-07-26.
// status: "partial" = a real sub-result, not a close · "wall" = tried hard,
// got nothing · "open" = probed, problem open, nothing to show as ours ·
// "refuted" = our own claim/conjecture died. seats: PRO = ChatGPT Pro /
// GPT-5.6 Sol reasoner briefs (relayed by Patrick) · CODEX = Codex at max
// reasoning (separate usage bucket, runs as parallel waves) · GROK = Grok
// Heavy decorrelation bake-offs.
const LEDGER_OFFSITE = [
  { n: 23, problem: "Triangle-free bipartite edge-bipartization", outcome: "No counterexample found — search exhausted its budget. Problem open.", status: "wall", seats: ["CODEX"], date: "2026-07-25" },
  { n: 28, problem: "Representation functions of asymptotic bases", outcome: "Early batch run — no verdict recovered (run JSON only).", status: "wall", seats: ["CODEX"], date: "2026-05-26" },
  { n: 39, problem: "Density of infinite Sidon sets", outcome: "Early batch run — no verdict recovered (run JSON only).", status: "wall", seats: ["CODEX"], date: "2026-05-26" },
  { n: 51, problem: "Least inverse-totient ratios", outcome: "No counterexample — ratio behavior verified computationally. Open.", status: "open", seats: ["CODEX"], date: "2026-07-25" },
  { n: 52, problem: "Erdős–Szemerédi sum-product", outcome: "Early batch run — no verdict recovered (run JSON only).", status: "wall", seats: ["CODEX"], date: "2026-05-26" },
  { n: 64, problem: "Erdős–Gyárfás powers-of-two graph problem", outcome: "Verifier built and checked; no verdict write-up was ever produced.", status: "wall", seats: ["CODEX"], date: "2026-05-26" },
  { n: 74, problem: "Infinite-chromatic bipartite graphs", outcome: "A reduction plus a conditional construction — no resolution. Open.", status: "open", seats: ["CODEX"], date: "2026-07-25" },
  { n: 97, problem: "Convex-position point sets", outcome: "The one that beat every model at every budget in our cross-model bench. Best outcome: an honest decline.", status: "wall", seats: ["PRO", "GROK", "CODEX"], date: "2026-05-26", rounds: 3 },
  { n: 126, problem: "Prime factors of pairwise sums", outcome: "Two rounds, decorrelated second opinions included — both unsolved.", status: "wall", seats: ["PRO", "GROK", "CODEX"], date: "2026-07-25", rounds: 2 },
  { n: 159, problem: "Ramsey numbers R(C₄, Kₜ)", outcome: "No polynomial improvement in either direction. Open ($100).", status: "wall", seats: ["CODEX"], date: "2026-07-25" },
  { n: 201, problem: "Worst-case progression-free subsets", outcome: "The requested limiting ratio was never proved. Open.", status: "open", seats: ["CODEX"], date: "2026-07-26" },
  { n: 256, problem: "Littlewood-type sup-norm bounds", outcome: "Computational upper bounds for f(4), f(5) verified. General problem open.", status: "partial", seats: ["CODEX"], date: "2026-05-26" },
  { n: 313, problem: "Unit-fraction sums and reciprocal primes", outcome: "New computational contribution landed; infinitude still open unconditionally.", status: "partial", seats: ["CODEX"], date: "2026-07-26" },
  { n: 345, problem: "Completeness thresholds for distinct powers", outcome: "Subset-sum checker built; the asymptotic threshold is unresolved.", status: "open", seats: ["CODEX"], date: "2026-07-26" },
  { n: 421, problem: "Sneiderman's conjecture (AND-graphs)", outcome: "Remote-witness obstruction unresolved; a blind reattempt corroborated the architecture, no summable bound.", status: "wall", seats: ["PRO", "CODEX"], date: "2026-07-25", rounds: 2 },
  { n: 445, problem: "Modular inverses in short intervals", outcome: "Search produced no proof claim. Open.", status: "open", seats: ["CODEX"], date: "2026-07-25" },
  { n: 475, problem: "Valid orderings in F_p", outcome: "Decidable up to the computed range, no counterexample — general case open.", status: "partial", seats: ["CODEX"], date: "2026-07-25" },
  { n: 486, problem: "Primitive sets and activated congruence sieves", outcome: "Sieve machinery explored; the full problem appears untouched. Open.", status: "open", seats: ["CODEX"], date: "2026-07-26" },
  { n: 488, problem: "Divisor-closed set densities", outcome: "Round 2: proofs for 3 and 4 primitive generators. General case open.", status: "partial", seats: ["CODEX"], date: "2026-07-25", rounds: 2 },
  { n: 530, problem: "Unavoidable Sidon subsets", outcome: "The order is already Θ(√N) — the refinement is the question. Open.", status: "open", seats: ["CODEX"], date: "2026-07-26" },
  { n: 611, problem: "Clique transversals", outcome: "Open — a related variant was solved by others (Joret–Micek–Reed–Smid) while we worked it.", status: "open", seats: ["CODEX"], date: "2026-07-26" },
  { n: 617, problem: "Rigidity in Ramsey r ≥ 5 constructions", outcome: "Two computational obstructions independently confirmed (affine K₂₅→K₂₆ nonexistent; non-rigidity).", status: "partial", seats: ["CODEX"], date: "2026-05-26" },
  { n: 686, problem: "A Diophantine non-representability claim", outcome: "Complete N=4, k=4 certificate — no integers m, n exist. Full problem stays open.", status: "partial", seats: ["PRO", "CODEX"], date: null },
  { n: 701, problem: "Chvátal's conjecture (intersecting down-set ideals)", outcome: "No counterexample, no general proof. Open.", status: "wall", seats: ["CODEX"], date: "2026-07-25" },
  { n: 708, problem: "Erdős–Surányi product covering", outcome: "Round 2 pins g(4) = 5. The asymptotic remains open.", status: "partial", seats: ["PRO", "GROK", "CODEX"], date: "2026-07-25", rounds: 2 },
  { n: 740, problem: "Infinite chromatic number with short odd cycles", outcome: "Literature map plus several open cases — no resolution.", status: "open", seats: ["CODEX"], date: "2026-07-26" },
  { n: 766, problem: "Minimum Turán numbers, small (k, ℓ)", outcome: "Counterexamples to eventual strictness found and checked. Unresolved.", status: "partial", seats: ["CODEX"], date: "2026-07-26" },
  { n: 773, problem: "Sidon subsets of the squares", outcome: "No proof of the N^(1−o(1)) bound. Open.", status: "open", seats: ["CODEX"], date: "2026-07-25" },
  { n: 805, problem: "Cliques and independent sets in induced subgraphs", outcome: "Two rounds — still open.", status: "wall", seats: ["CODEX"], date: "2026-07-25", rounds: 2 },
  { n: 972, problem: "Primes at prime indices in Beatty sequences", outcome: "Strong partial — the universal statement remains open.", status: "partial", seats: ["CODEX"], date: "2026-07-25" },
  { n: 993, problem: "Non-unimodal independence-polynomial trees", outcome: "Found non-log-concave trees, but still unimodal — the target was never met across 11 search runs.", status: "wall", seats: ["CODEX"], date: "2026-05-26", rounds: 4 },
  { n: 1061, problem: "Additive identities for the divisor sum", outcome: "Open — a recent Eric Li preprint claims more; we treat it as an external candidate, not ours.", status: "open", seats: ["CODEX"], date: "2026-07-25" },
  { n: 1139, problem: "Large gaps between integers with Ω(n) ≤ 2", outcome: "Strong partial, verified — not closed by us (Price's claimed proof is unauditable).", status: "partial", seats: ["PRO"], date: null, rounds: 2 },
];

// ---------------------------------------------------------------------------
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function formatDate(iso) {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" });
}

// Site launch date — Day 1 — is Patrick's #477 close (2026-07-23 MDT, just
// before midnight; the site itself launched ~6 minutes later, 23:54 MDT,
// which is already past midnight UTC and reads as "2026-07-24" in git/UTC
// terms). dayNumber() counts real elapsed calendar days in HIS timezone
// (America/Denver, MDT/MST), not UTC and not distinct entries.date values
// — it used to do the latter, which meant it stuck at 1 forever until a
// second date appeared, AND an earlier UTC-anchored version undercounted
// by a day relative to Patrick's own lived calendar. Caught live 2026-07-24
// when he said "oh but I think we did 477 yesterday my time" — he was
// right on both counts.
const LAUNCH_DATE = "2026-07-23";
const SITE_TIMEZONE = "America/Denver";
function todayInTimezone(tz) {
  // en-CA gives YYYY-MM-DD directly, sidestepping locale ordering games.
  return new Date().toLocaleDateString("en-CA", { timeZone: tz });
}
function dayNumber() {
  const launch = new Date(LAUNCH_DATE + "T00:00:00Z");
  const today = new Date(todayInTimezone(SITE_TIMEZONE) + "T00:00:00Z");
  const days = Math.floor((today.getTime() - launch.getTime()) / 86400000) + 1;
  return Math.max(1, days);
}

function statusBadge(statusKey) {
  const s = STATUS[statusKey];
  const pulse = statusKey === "in_progress" ? `<span class="pulse-dot"></span>` : "";
  return `<span class="badge badge-${s.cls}">${pulse}${escapeHtml(s.badge)}</span>`;
}

// ---------------------------------------------------------------------------
// THE UNIFIED LEDGER. Every numbered problem we've touched, one record,
// merged from three sources and deduplicated by problem number (a shipped
// /day/ entry always wins over an internal row for the same number):
//   1. `entries`        — full write-ups, each with its own /day/ page
//   2. `LEDGER`         — generated working reports (churn waves), each with /report/<n>
//   3. `LEDGER_OFFSITE` — the early internal attempts, hand-maintained one-liners
// Each row gets a BOX (one of the six filter buckets on the homepage) and a
// BADGE (the honest per-row label, finer than the box — e.g. a run stopped by
// the no-collision rule counts in the WALL box but wears SKIPPED on the row,
// because we never actually attempted it).
const BOX = {
  all:        { label: "ATTEMPTED",        cls: "tackled" },
  closed:     { label: "CLOSED",           cls: "closed" },
  closedbyus: { label: "CLOSED BY US",     cls: "closedbyus" },
  partial:    { label: "VERIFIED PARTIAL", cls: "confirmed" },
  live:       { label: "LIVE",             cls: "live" },
  wall:       { label: "WALL",             cls: "noproof" },
};

// Badge vocabulary for working-report + offsite rows. PROVED/FOUND wear gold
// (a decisive verified check) while still counting in the VERIFIED PARTIAL
// box — they close a statement, not the problem.
const CHIP = {
  PROVED:      { cls: "closed",  label: "PROVED" },
  FOUND:       { cls: "closed",  label: "FOUND" },
  PARTIAL:     { cls: "partial", label: "PARTIAL" },
  WALL:        { cls: "noproof", label: "WALL" },
  SKIP:        { cls: "noproof", label: "SKIPPED" },
  NO_PROGRESS: { cls: "wall",    label: "NO PROGRESS" },
};

// Churn FOUND/PROVED verdicts that are actually literature-closes — we located
// and audited someone ELSE's solution, so the problem counts as CLOSED (not by
// us). The generator can't tell these apart; hand-maintained, one line each.
const CLOSED_BY_LITERATURE = new Set([
  1199, // exact affirmative solution in arXiv:2607.17333v2; our audit found no gap
]);

// HEADLINES — the discovery-tier results that must NOT render as just another
// "read the working report" card in the firehose. Hand-maintained (like
// CLOSED_BY_LITERATURE): the generator can't tell a once-in-a-session discovery
// from a routine exact-table partial. One line each, FACTUAL + HONESTLY
// ATTRIBUTED — whose result it is, and what is / isn't claimed. The front page's
// whole register is "watch me vibe-math my way to discoveries"; without this band
// the discoveries are invisible at the surface. hrefs point at /report/<n> until a
// full /day/ writeup exists (those are drafted, not auto-promoted).
const HEADLINES = [
  {
    n: 1199, kind: "solved", tag: "SOLVED · NOT BY US",
    title: "A 50-year-old open problem, solved — and the tracker never noticed",
    line: "Owings's 1974 two-colour sumset question was answered affirmatively eight " +
      "days ago (Huang–Lian–Shao–Xiao–Xu–Zhang, arXiv:2607.17333). The live page still " +
      "said OPEN. We found the preprint, audited the proof (digest-pinned v2, no gap " +
      "modulo the named Stone–Čech inputs), and independently certified R_Σ(1..3)=" +
      "(1,7,23). The theorem is theirs; the catch and the audit are ours.",
    href: "/report/1199",
  },
  {
    n: 709, kind: "bound", tag: "RE-CHECKED PUBLIC PROOF · + TRANSFER",
    title: "Upper bound re-checked against a public Lean proof; we add the lower-bound transfer",
    line: "The 3/7 upper bound is NOT new to us: a public Star Fleet Math bundle " +
      "(14 Jul 2026, starfleetmath.com) states it with a Lean 4 formalization of the same " +
      "four-projection proof. We independently reconstructed the finite argument, audited " +
      "the Lean sources (no sorries; full Mathlib rebuild not run), and tightened the " +
      "rounding trivially — so no priority claim, matching the report's own stance. The " +
      "genuinely new bit is the lower-bound transfer from Kominers 2607.10431 → " +
      "(1/e−o(1))log n, which the live page omits.",
    href: "/report/709",
  },
  {
    n: 684, kind: "defect", tag: "FALSE LEMMA CAUGHT",
    title: "A live preprint's key lemma is false — we have the counterexample",
    line: "Bae's arXiv:2604.23784 (April; claims #684) rests on Lemma 18, which is " +
      "false: a counterexample built in the paper's own definitions, deterministic " +
      "checker green, the A_p definition and θ-condition matched verbatim against the " +
      "source. The unbounded-limsup corollary falls with it. A note to the tracker / " +
      "the author is the next step — Patrick's call.",
    href: "/report/684",
  },
];

function boxForEntry(e) {
  if (e.status === "proof_claimed" || e.status === "posted") return "closed";
  if (e.status === "partial") return "partial";
  if (e.status === "in_progress") return "live";
  return "wall"; // declined, refuted — tried honestly, nothing verified landed
}

function ledgerRows() {
  const rows = [];
  const taken = new Set();
  for (const e of entries) {
    taken.add(e.problemNum);
    rows.push({
      kind: "writeup", n: e.problemNum, date: e.date,
      box: boxForEntry(e),
      cb: (e.status === "proof_claimed" && e.originatedByUs) ? 1 : 0,
      isToday: false, e,
    });
  }
  for (const r of LEDGER) {
    if (taken.has(r.n)) continue;
    taken.add(r.n);
    const decisive = r.verdict === "PROVED" || r.verdict === "FOUND";
    const box = CLOSED_BY_LITERATURE.has(r.n) ? "closed"
      : (decisive || r.verdict === "PARTIAL") ? "partial"
      : "wall";
    rows.push({ kind: "report", n: r.n, date: r.d || "", box, cb: 0, hl: HEADLINES.some((h) => h.n === r.n), r });
  }
  for (const o of LEDGER_OFFSITE) {
    if (taken.has(o.n)) continue;
    taken.add(o.n);
    rows.push({
      kind: "offsite", n: o.n, date: o.date || "",
      box: o.status === "partial" ? "partial" : "wall", cb: 0, o,
    });
  }
  rows.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : b.n - a.n));
  return rows;
}

function ledgerItemHtml(row) {
  if (row.kind === "writeup") {
    const e = row.e;
    return `
    <div class="record-item${row.isToday ? " is-today" : ""}" data-status="${row.box}" data-cb="${row.cb}">
      <div class="meta">ERD&#337;S #${e.problemNum} &middot; ${formatDate(e.date).toUpperCase()}</div>
      <h3><a href="/day/${e.slug}">${escapeHtml(e.title)}</a></h3>
      <p class="summary">${escapeHtml(e.summary)}</p>
      ${statusBadge(e.status)}<span class="tag-writeup">FULL WRITE-UP</span>
    </div>`;
  }
  if (row.kind === "report") {
    const r = row.r;
    const chip = CHIP[r.verdict] || CHIP.WALL;
    return `
    <div class="record-item${row.hl ? " is-headline" : ""}" data-status="${row.box}" data-cb="0" data-verdict="${r.verdict}">
      <div class="meta">ERD&#337;S #${r.n} &middot; ${r.d ? formatDate(r.d).toUpperCase() : "UNDATED"}</div>
      <h3><a href="/report/${r.n}">#${r.n} &mdash; read the working report &#8599;</a></h3>
      <p class="summary">${escapeHtml(r.gist)}</p>
      <span class="badge badge-${chip.cls}">${chip.label}</span>
    </div>`;
  }
  const o = row.o;
  const chip = o.status === "partial" ? CHIP.PARTIAL : o.status === "wall" ? CHIP.WALL : CHIP.NO_PROGRESS;
  const seats = o.seats && o.seats.length
    ? ` &middot; ${o.seats.map(escapeHtml).join(" + ")}${o.rounds ? ` &middot; ${o.rounds} ROUNDS` : ""}`
    : "";
  return `
    <div class="record-item" data-status="${row.box}" data-cb="0">
      <div class="meta">ERD&#337;S #${o.n} &middot; ${o.date ? formatDate(o.date).toUpperCase() : "UNDATED"}${seats}</div>
      <h3><a href="${CREDIT_URL}/${o.n}" target="_blank" rel="noopener">${escapeHtml(o.problem)} &#8599;</a></h3>
      <p class="summary">${escapeHtml(o.outcome)}</p>
      <span class="badge badge-${chip.cls}">${chip.label}</span>
    </div>`;
}

function ledgerScoreboard(rows) {
  const count = (k) => k === "all" ? rows.length
    : k === "closedbyus" ? rows.filter((r) => r.cb === 1).length
    : rows.filter((r) => r.box === k).length;
  const boxes = Object.keys(BOX).map((k) => {
    const b = BOX[k];
    const pulse = k === "live" ? `<span class="pulse-dot"></span>` : "";
    return `<div class="stat-box stat-${b.cls}" data-filter="${k}" data-label="${b.label}" role="button" tabindex="0" aria-pressed="false"><div class="stat-value">${count(k)}</div><div class="stat-label">${pulse}${b.label}</div></div>`;
  }).join("");
  return `<div class="stats-strip">
    ${boxes}
  </div>
  <div class="filter-hint">tap any box to filter the ledger &middot; tap it again to clear</div>`;
}

// ---------------------------------------------------------------------------
function css() {
  return `
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Teko:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
  --bg-base: #050507; --bg-panel: #111216; --bg-panel-hover: #18191e;
  --border-dim: #2a2d36;
  --text-main: #d1d5db; --text-muted: #8b92a5; --text-bright: #ffffff;
  --gold: #ffb703; --gold-glow: rgba(255, 183, 3, 0.6);
  --blue: #00f0ff; --blue-glow: rgba(0, 240, 255, 0.6);
  --green: #39ff88; --green-glow: rgba(57, 255, 136, 0.5);
  --red: #ff0055; --red-glow: rgba(255, 0, 85, 0.5);
  --gray: #6b7280;
  --amber: #ff8a33; --amber-glow: rgba(255,138,51,.5);
}
* { box-sizing: border-box; }
body {
  margin: 0; font-family: 'Rajdhani', sans-serif;
  background-color: var(--bg-base); color: var(--text-main); line-height: 1.55;
  background-image:
    linear-gradient(rgba(17,18,22,.8) 1px, transparent 1px),
    linear-gradient(90deg, rgba(17,18,22,.8) 1px, transparent 1px);
  background-size: 40px 40px; background-position: center top; background-attachment: fixed;
  -webkit-font-smoothing: antialiased;
}
h1, h2, h3, .font-display { font-family: 'Teko', sans-serif; text-transform: uppercase; line-height: 1; color: var(--text-bright); font-weight: 600; }
.mono { font-family: 'JetBrains Mono', monospace; }
a { color: var(--gold); }
.wrap { max-width: 900px; margin: 0 auto; padding: 2rem 1.25rem 5rem; }

header.site { display: flex; align-items: center; justify-content: space-between; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-dim); margin-bottom: 2.5rem; flex-wrap: wrap; gap: .75rem; }
header.site .mark { font-family: 'Teko', sans-serif; font-size: 1.8rem; font-weight: 600; letter-spacing: 1px; text-decoration: none; color: var(--text-bright); text-transform: uppercase; }
header.site .mark .gold { color: var(--gold); text-shadow: 0 0 12px var(--gold-glow); }
header.site nav a { font-family: 'Rajdhani',sans-serif; color: var(--text-muted); text-decoration: none; margin-left: 1.5rem; font-size: .95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
header.site nav a:hover { color: var(--blue); }
header.site .nav-toggle {
  display: none; background: none; border: 1px solid var(--border-dim); color: var(--text-bright);
  font-size: 1.3rem; line-height: 1; padding: .3rem .65rem; border-radius: 4px; cursor: pointer;
}
header.site .nav-toggle:hover { color: var(--blue); border-color: var(--blue); }

.hero { text-align: left; margin-bottom: 2.5rem; }
.kicker { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: .72rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--blue); border: 1px solid var(--blue); background: rgba(0,240,255,.06); padding: .3rem .7rem; border-radius: 2px; margin-bottom: 1.2rem; }
h1.hero-h1 { font-size: clamp(2.6rem, 7vw, 4.2rem); letter-spacing: -.5px; margin: 0 0 1.1rem; }
h1.hero-h1 .gold { color: var(--gold); text-shadow: 0 0 20px var(--gold-glow), 0 0 40px var(--gold); }
.hero-sub { font-family: 'Rajdhani', sans-serif; font-size: 1.15rem; font-weight: 500; color: var(--text-muted); max-width: 62ch; margin: 0 0 1.5rem; }
.hero-links { display: flex; gap: 1.5rem; flex-wrap: wrap; font-family: 'Rajdhani',sans-serif; font-weight: 700; font-size: .95rem; text-transform: uppercase; letter-spacing: .5px; }
.hero-links a { text-decoration: none; color: var(--gold); }
.hero-links a:hover { text-decoration: underline; }

.stats-strip { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px,1fr)); gap: 2px; background: var(--border-dim); border: 1px solid var(--border-dim); margin: 2rem 0; transform: skewX(-5deg); }
.stat-box { background: var(--bg-panel); padding: 1.5rem 1rem; text-align: center; transform: skewX(5deg); }
.stat-value { font-family: 'Teko', sans-serif; font-size: clamp(2.2rem, 5vw, 3.2rem); font-weight: 600; color: var(--text-bright); line-height: 1; }
.stat-label { font-family: 'JetBrains Mono', monospace; font-size: .72rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--text-muted); margin-top: .3rem; }
.stat-closed .stat-value { color: var(--gold); text-shadow: 0 0 15px var(--gold-glow); }
.stat-closedbyus .stat-value { color: var(--gold); text-shadow: 0 0 15px var(--gold-glow); }
.stat-closedbyus .stat-label { color: var(--text-muted); }
.stat-confirmed .stat-value { color: var(--green); text-shadow: 0 0 15px var(--green-glow); }
.stat-refuted .stat-value { color: var(--red); text-shadow: 0 0 15px var(--red-glow); }
.stat-noproof .stat-value { color: var(--gray); }
.stat-live { position: relative; overflow: hidden; }
.stat-live::before { content: ''; position: absolute; top:0; left:0; right:0; height:2px; background: var(--blue); box-shadow: 0 0 10px var(--blue); }
.stat-live .stat-value { color: var(--blue); text-shadow: 0 0 15px var(--blue-glow); animation: pulse-text 2s infinite; }
.stat-live .stat-label { color: var(--text-bright); }
.stat-box { cursor: pointer; }
.stat-box:hover { background: var(--bg-panel-hover); }
.stat-box:focus-visible { outline: 2px solid var(--blue); outline-offset: -2px; }
.stat-box.active { outline: 2px solid var(--gold); outline-offset: -3px; background: var(--bg-panel-hover); box-shadow: inset 0 0 26px rgba(255,183,3,.10); }
.stat-box.active .stat-label { color: var(--text-bright); }
.stat-partial .stat-value { color: var(--amber); text-shadow: 0 0 15px var(--amber-glow); }
.stat-partial { position: relative; overflow: hidden; }
.stat-partial::before { content: ''; position: absolute; top:0; left:0; right:0; height:2px; background: var(--amber); box-shadow: 0 0 10px var(--amber); }
.stat-tackled .stat-value { color: var(--text-bright); }
.filter-hint { font-family: 'JetBrains Mono', monospace; font-size: .66rem; letter-spacing: .12em; text-transform: uppercase; color: var(--text-muted); text-align: center; margin: -1.1rem 0 1.7rem; transform: skewX(-5deg); opacity: .85; }
.filter-bar { display: flex; align-items: center; justify-content: space-between; gap: 1rem; font-family: 'JetBrains Mono', monospace; font-size: .76rem; letter-spacing: .08em; text-transform: uppercase; color: var(--amber); border: 1px solid var(--amber); background: rgba(255,138,51,.07); padding: .6rem 1rem; margin: 0 0 1.1rem; transform: skewX(-5deg); box-shadow: 0 0 18px rgba(255,138,51,.12); }
.filter-bar[hidden] { display: none; }
.filter-bar > * { transform: skewX(5deg); }
.filter-bar #filterBarText { color: var(--amber); text-shadow: 0 0 10px var(--amber-glow); }
.filter-bar button { background: none; border: 1px solid var(--border-dim); color: var(--text-muted); font: inherit; cursor: pointer; padding: .25rem .7rem; letter-spacing: .06em; }
.filter-bar button:hover { color: var(--blue); border-color: var(--blue); }

.pulse-dot { display: inline-block; width: 8px; height: 8px; background: var(--blue); border-radius: 50%; margin-right: 6px; box-shadow: 0 0 8px var(--blue); animation: pulse-dot-anim 1.5s infinite; vertical-align: middle; }

.section-header { display: flex; align-items: center; gap: 1rem; margin: 2.75rem 0 1.25rem; }
.section-header h2 { font-size: 1.9rem; letter-spacing: 1px; white-space: nowrap; }
.section-header .line { flex-grow: 1; height: 1px; background: linear-gradient(90deg, var(--border-dim), transparent); }

.target-card { background: var(--bg-panel); border: 1px solid var(--border-dim); border-left: 4px solid var(--blue); padding: 1.75rem 2rem; position: relative; margin-bottom: 1rem; box-shadow: inset 0 0 50px rgba(0,240,255,.05); }
.target-card::after { content: ''; position: absolute; top:-1px; left:-1px; width:26px; height:26px; border-top: 2px solid var(--blue); border-left: 2px solid var(--blue); }
.target-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: .8rem; font-family: 'JetBrains Mono', monospace; font-size: .8rem; font-weight: 700; color: var(--text-muted); letter-spacing: 1px; text-transform: uppercase; flex-wrap: wrap; gap: .5rem; }
.target-card h3 { font-size: 2.1rem; margin: 0 0 .6rem; font-weight: 600; }
.target-card h3 a { color: var(--text-bright); text-decoration: none; }
.target-card h3 a:hover { color: var(--blue); }
.target-card .summary { font-family: 'Rajdhani',sans-serif; font-size: 1.05rem; color: var(--text-main); margin: 0 0 1.1rem; }
.target-card .cta { display: inline-block; border: 1px solid var(--blue); color: var(--blue); font-family:'Rajdhani',sans-serif; padding: .55rem 1.4rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; text-decoration: none; box-shadow: 0 0 10px rgba(0,240,255,.2); }
.target-card .cta:hover { background: var(--blue); color: #000; box-shadow: 0 0 20px rgba(0,240,255,.6); }
.headlines { display: grid; gap: 1rem; }
.headline-card { background: var(--bg-panel); border: 1px solid var(--border-dim); border-left: 4px solid var(--blue); padding: 1.4rem 1.6rem; position: relative; box-shadow: inset 0 0 40px rgba(0,240,255,.04); transition: all .15s ease; }
.headline-card:hover { background: var(--bg-panel-hover); transform: translateX(4px); }
.headline-card .hl-tag { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: .7rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; border: 1px solid; padding: .25rem .6rem; border-radius: 2px; margin-bottom: .7rem; }
.headline-card .hl-meta { font-family: 'JetBrains Mono', monospace; font-size: .72rem; color: var(--text-muted); letter-spacing: .5px; margin-bottom: .3rem; }
.headline-card h3 { font-size: 1.55rem; margin: 0 0 .5rem; font-weight: 600; }
.headline-card h3 a { color: var(--text-bright); text-decoration: none; }
.headline-card h3 a:hover { color: var(--gold); }
.headline-card .summary { font-family: 'Rajdhani', sans-serif; color: var(--text-main); font-size: 1.02rem; margin: 0 0 1rem; line-height: 1.45; }
.headline-card .cta { display: inline-block; border: 1px solid; padding: .45rem 1.1rem; font-family: 'Rajdhani', sans-serif; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; text-decoration: none; font-size: .85rem; }

.record-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 1rem; }
.record-item { background: var(--bg-panel); border: 1px solid var(--border-dim); padding: 1.1rem 1.4rem; transition: all .15s ease; }
.record-item:hover { background: var(--bg-panel-hover); border-color: #3b404d; transform: translateX(4px); }
.record-item .meta { font-family: 'JetBrains Mono', monospace; font-size: .75rem; color: var(--text-muted); letter-spacing: .5px; margin-bottom: .4rem; }
.record-item h3 { font-size: 1.5rem; font-weight: 600; margin: 0 0 .4rem; }
.record-item h3 a { color: var(--text-bright); text-decoration: none; }
.record-item h3 a:hover { color: var(--gold); }
.record-item .summary { font-family: 'Rajdhani',sans-serif; color: var(--text-muted); margin: 0 0 .7rem; font-size: .98rem; }

.badge { display: inline-flex; align-items: center; font-family: 'JetBrains Mono', monospace; padding: .25rem .7rem; font-size: .74rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; border-radius: 2px; }
.badge-closed { background: rgba(255,183,3,.1); color: var(--gold); border: 1px solid var(--gold); }
.badge-confirmed { background: rgba(57,255,136,.1); color: var(--green); border: 1px solid var(--green); }
.badge-live { background: rgba(0,240,255,.1); color: var(--blue); border: 1px solid var(--blue); animation: border-pulse 2s infinite; }
.badge-refuted { background: rgba(255,0,85,.1); color: var(--red); border: 1px solid var(--red); }
.badge-noproof { background: rgba(107,114,128,.1); color: var(--gray); border: 1px solid var(--gray); }

.problem-num { font-family: 'JetBrains Mono', monospace; color: var(--text-muted); font-size: .85rem; letter-spacing: .5px; }
article h1 { font-size: clamp(2rem, 5vw, 2.8rem); margin: .4rem 0 1rem; text-transform: none; }
article .meta-row { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; margin-bottom: 1.5rem; }
article .meta-row .date { font-family: 'JetBrains Mono', monospace; color: var(--text-muted); font-size: .85rem; }
article .body-content { font-family: 'Rajdhani', sans-serif; font-size: 1.08rem; }
article .body-content p { margin: 0 0 1.1rem; }
article .body-content strong { color: var(--text-bright); }
article .body-content em { color: var(--gold); font-style: normal; }
.links-list { font-family: 'Rajdhani',sans-serif; font-size: .95rem; margin-top: 1.5rem; padding-top: 1.2rem; border-top: 1px solid var(--border-dim); }
.links-list a { display: block; margin: .35rem 0; font-weight: 700; text-decoration: none; }
.links-list a:hover { text-decoration: underline; }
.links-heading { font-family: 'JetBrains Mono', monospace; font-size: .66rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .5rem; }
.lh-receipt { color: var(--gold); }
.lh-source { color: var(--text-muted); }
.links-list + .links-list { margin-top: 1.1rem; padding-top: 0; border-top: none; }

footer.site { margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--border-dim); font-family: 'Rajdhani',sans-serif; font-size: .85rem; color: var(--text-muted); }
footer.site a { color: var(--text-muted); font-weight: 700; }
footer.site a:hover { color: var(--gold); }

.about-block { font-family: 'Rajdhani', sans-serif; font-size: 1.02rem; }
.status-def { margin-bottom: 1rem; display: flex; gap: 1rem; align-items: baseline; }
.status-def .badge { flex-shrink: 0; }
.also-queued { font-family: 'Rajdhani',sans-serif; font-size: .92rem; color: var(--text-muted); margin-top: .5rem; }
.also-queued a { font-weight: 700; }

.ledger-note { font-family: 'Rajdhani', sans-serif; color: var(--text-muted); font-size: .95rem; margin: 0 0 1.25rem; max-width: 72ch; }
.ledger-row { display: grid; grid-template-columns: 74px 1fr auto; gap: 1.1rem; align-items: center; background: var(--bg-panel); border: 1px solid var(--border-dim); padding: .85rem 1.25rem; margin-bottom: 6px; transition: all .15s ease; }
.ledger-row:hover { background: var(--bg-panel-hover); transform: translateX(4px); }
.ledger-row.st-closed { border-left: 4px solid var(--gold); }
.ledger-row.st-partial { border-left: 4px solid var(--amber); }
.ledger-row.st-wall { border-left: 4px solid var(--gray); }
.ledger-row.st-open { border-left: 4px solid var(--blue); }
.ledger-row.st-refuted { border-left: 4px solid var(--red); }
.ledger-num { font-family: 'Teko', sans-serif; font-size: 2rem; font-weight: 600; color: var(--text-bright); line-height: .9; text-align: center; }
.ledger-num .hash { color: var(--text-muted); font-size: 1.2rem; }
.ledger-num .sub { display: block; font-family: 'JetBrains Mono', monospace; font-size: .58rem; font-weight: 700; color: var(--text-muted); letter-spacing: .12em; margin-top: .25rem; }
.ledger-main h3 { font-family: 'Rajdhani', sans-serif; text-transform: none; letter-spacing: 0; line-height: 1.3; font-size: 1.02rem; font-weight: 700; color: var(--text-bright); margin: 0 0 .2rem; }
.ledger-main h3 a { color: var(--text-bright); text-decoration: none; }
.ledger-main h3 a:hover { color: var(--gold); }
.ledger-main .outcome { font-family: 'Rajdhani', sans-serif; color: var(--text-muted); font-size: .92rem; margin: 0 0 .4rem; }
.ledger-tags { display: flex; gap: .4rem; flex-wrap: wrap; align-items: center; }
.chip { font-family: 'JetBrains Mono', monospace; font-size: .6rem; font-weight: 700; letter-spacing: .08em; padding: .13rem .5rem; border: 1px solid var(--border-dim); color: var(--text-muted); border-radius: 2px; white-space: nowrap; }
.chip-pro { border-color: var(--gold); color: var(--gold); }
.chip-codex { border-color: var(--blue); color: var(--blue); }
.chip-grok { border-color: var(--green); color: var(--green); }
.chip-rounds { border-style: dashed; }
.ledger-side { display: flex; flex-direction: column; gap: .4rem; align-items: flex-end; }
.ledger-date { font-family: 'JetBrains Mono', monospace; font-size: .68rem; color: var(--text-muted); letter-spacing: .05em; }
.badge-partial { background: rgba(255,138,51,.10); color: var(--amber); border: 1px solid var(--amber); }
.badge-wall { background: rgba(107,114,128,.12); color: var(--gray); border: 1px solid var(--gray); }
.badge-open { background: rgba(0,240,255,.08); color: var(--blue); border: 1px solid var(--blue); }
.tag-writeup { display: inline-flex; align-items: center; font-family: 'JetBrains Mono', monospace; padding: .25rem .7rem; font-size: .74rem; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; border-radius: 2px; margin-left: .5rem; background: rgba(255,255,255,.05); color: var(--text-bright); border: 1px solid #565d6e; }
.seat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 8px; margin-bottom: 1.25rem; }
.seat-card { background: var(--bg-panel); border: 1px solid var(--border-dim); padding: 1rem 1.15rem; }
.seat-card h4 { font-family: 'JetBrains Mono', monospace; font-size: .75rem; font-weight: 700; letter-spacing: .1em; margin: 0 0 .45rem; text-transform: uppercase; }
.seat-card.seat-pro h4 { color: var(--gold); }
.seat-card.seat-codex h4 { color: var(--blue); }
.seat-card.seat-grok h4 { color: var(--green); }
.seat-card.seat-claude h4 { color: var(--red); }
.seat-card p { font-family: 'Rajdhani', sans-serif; font-size: .88rem; color: var(--text-muted); margin: 0; line-height: 1.45; }
@media (max-width: 640px) {
  .ledger-row { grid-template-columns: 58px 1fr; }
  .ledger-side { grid-column: 2; flex-direction: row; align-items: center; gap: .75rem; }
  .ledger-num { font-size: 1.7rem; }
}

@keyframes pulse-text { 0%,100% { opacity:1; text-shadow: 0 0 15px var(--blue-glow); } 50% { opacity:.8; text-shadow: 0 0 5px rgba(0,240,255,.3); } }
@keyframes pulse-dot-anim { 0% { transform: scale(.95); box-shadow: 0 0 0 0 rgba(0,240,255,.7); } 70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0,240,255,0); } 100% { transform: scale(.95); box-shadow: 0 0 0 0 rgba(0,240,255,0); } }
@keyframes border-pulse { 0%,100% { border-color: rgba(0,240,255,1); box-shadow: 0 0 8px rgba(0,240,255,.4); } 50% { border-color: rgba(0,240,255,.3); box-shadow: none; } }

@media (max-width: 640px) {
  .stats-strip { grid-template-columns: repeat(2,1fr); transform: none; }
  .stat-box { transform: none; border-bottom: 1px solid var(--border-dim); border-right: 1px solid var(--border-dim); }
  .target-card { padding: 1.4rem; }

  header.site .nav-toggle { display: block; }
  header.site nav {
    display: none; order: 3; width: 100%; flex-direction: column; gap: 0;
    margin-top: .5rem; border-top: 1px solid var(--border-dim);
  }
  header.site.nav-open { padding-bottom: 0; }
  header.site.nav-open nav { display: flex; }
  header.site nav a { margin-left: 0; padding: .75rem 0; border-bottom: 1px solid var(--border-dim); }
  header.site nav a:last-child { border-bottom: none; padding-bottom: 1.5rem; }
}
`;
}

// ---------------------------------------------------------------------------
function layout({ title, description, path, body }) {
  const canonical = `https://erdosproblemaday.com${path}`;
  const ogImage = "https://erdosproblemaday.com/og-image.jpg";
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escapeHtml(title)}</title>
<meta name="description" content="${escapeHtml(description)}">
<link rel="canonical" href="${canonical}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta property="og:title" content="${escapeHtml(title)}">
<meta property="og:description" content="${escapeHtml(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="${canonical}">
<meta property="og:image" content="${ogImage}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="${ogImage}">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DTKRWBYKMH"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-DTKRWBYKMH');
</script>
<style>${css()}</style>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script defer>
document.addEventListener('DOMContentLoaded', function () {
  if (typeof renderMathInElement === 'function') {
    var B = String.fromCharCode(92);
    renderMathInElement(document.body, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: B + '[', right: B + ']', display: true },
        { left: B + '(', right: B + ')', display: false }
      ],
      throwOnError: false
    });
  }
});
</script>
<style>
.body-content{max-width:46rem;margin:1.5rem auto 0;font-family:'Rajdhani',system-ui,sans-serif;font-size:1.12rem;line-height:1.72;color:var(--text-main)}
.body-content h2,.body-content h3,.body-content h4{font-family:'Teko','Rajdhani',sans-serif;letter-spacing:.4px;color:var(--text-bright);line-height:1.08;margin:1.9rem 0 .55rem}
.body-content h2{font-size:2rem;border-bottom:1px solid var(--border-dim);padding-bottom:.3rem}
.body-content h3{font-size:1.5rem}
.body-content h4{font-size:1.18rem;text-transform:uppercase;letter-spacing:1px;color:var(--blue)}
.body-content p{margin:0 0 1.05rem}
.body-content ul,.body-content ol{margin:0 0 1.1rem;padding-left:1.5rem}
.body-content li{margin:.3rem 0}
.body-content a{color:var(--blue);text-decoration:none;border-bottom:1px solid rgba(0,240,255,.35)}
.body-content a:hover{color:var(--gold);border-color:var(--gold)}
.body-content code{font-family:'JetBrains Mono',monospace;font-size:.9em;background:rgba(255,255,255,.07);padding:.12em .4em;border-radius:4px}
.body-content pre{background:rgba(0,0,0,.4);border:1px solid var(--border-dim);border-radius:8px;padding:1rem 1.1rem;overflow-x:auto;margin:0 0 1.3rem}
.body-content pre code{background:none;padding:0}
.body-content .math-block{margin:1.3rem 0;overflow-x:auto;overflow-y:hidden;padding:.2rem 0}
.body-content .katex-display{margin:1.1rem 0}
.body-content .katex{color:var(--text-bright)}
</style>
</head>
<body>
<div class="wrap">
<header class="site">
  <a class="mark" href="/">ERDŐS/DAILY <span class="gold">▸</span></a>
  <button class="nav-toggle" aria-label="Menu" aria-expanded="false">☰</button>
  <nav><a href="/">The Ledger</a><a href="/friends">Friends We Made</a><a href="/scouting">How We Pick</a><a href="/about">About</a></nav>
</header>
${body}
<footer class="site">
  Patrick White + Claude (Anthropic), in public — AI-disclosed on every entry.
  Problems from <a href="${CREDIT_URL}" target="_blank" rel="noopener">T. F. Bloom's erdosproblems.com</a>,
  full credit, no competing list — we only post there once a result clears its own bar. ·
  <a href="${VIBE_MATHING_URL}" target="_blank" rel="noopener">The full vibe-mathing story</a> ·
  <a href="/about">How this works</a>
</footer>
</div>
<script>
(function() {
  var btn = document.querySelector('.nav-toggle');
  var header = document.querySelector('header.site');
  if (!btn || !header) return;
  btn.addEventListener('click', function() {
    var open = header.classList.toggle('nav-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
</script>
<script>
(function(){
  var list = document.getElementById('recordList');
  if (!list) return;
  var items = Array.prototype.slice.call(list.querySelectorAll('.record-item'));
  var boxes = Array.prototype.slice.call(document.querySelectorAll('.stat-box[data-filter]'));
  var bar = document.getElementById('filterBar');
  var barText = document.getElementById('filterBarText');
  var clearBtn = document.getElementById('filterClear');
  var today = Array.prototype.slice.call(document.querySelectorAll('.js-today'));
  var current = 'all';
  function boxFor(k){ for (var i=0;i<boxes.length;i++){ if (boxes[i].getAttribute('data-filter')===k) return boxes[i]; } return null; }
  function labelFor(k){ var b = boxFor(k); return b ? b.getAttribute('data-label') : k; }
  function matches(it, k){ if (k==='all') return !it.classList.contains('is-today') && !it.classList.contains('is-headline') && it.getAttribute('data-verdict')!=='SKIP'; if (k==='closedbyus') return it.getAttribute('data-cb')==='1'; return it.getAttribute('data-status')===k; }
  function setView(k){
    current = k;
    var filtering = (k !== 'all');
    document.body.classList.toggle('filtering', filtering);
    today.forEach(function(el){ el.style.display = filtering ? 'none' : ''; });
    if (bar) bar.hidden = !filtering;
    var n = 0;
    items.forEach(function(it){ var show = matches(it, k); if (show) n++; it.style.display = show ? '' : 'none'; });
    if (barText) barText.textContent = filtering ? ('SHOWING ' + labelFor(k) + '  ·  ' + n + (n===1?' ENTRY':' ENTRIES')) : '';
    boxes.forEach(function(b){ var on = b.getAttribute('data-filter')===k; b.classList.toggle('active', on); b.setAttribute('aria-pressed', on?'true':'false'); });
  }
  function handler(b){ return function(ev){ if (ev.type==='keydown'){ if (ev.key!=='Enter' && ev.key!==' ' && ev.keyCode!==13 && ev.keyCode!==32) return; ev.preventDefault(); } var k = b.getAttribute('data-filter'); setView((current===k && k!=='all') ? 'all' : k); }; }
  boxes.forEach(function(b){ b.addEventListener('click', handler(b)); b.addEventListener('keydown', handler(b)); });
  if (clearBtn) clearBtn.addEventListener('click', function(){ setView('all'); });
  setView('all');
})();
</script>
</body>
</html>`;
}

// ---------------------------------------------------------------------------
function headlinesHtml() {
  const ACCENT = { solved: "var(--gold)", bound: "var(--blue)", defect: "var(--amber)" };
  const cards = HEADLINES.map((h) => {
    const a = ACCENT[h.kind] || "var(--blue)";
    return `
    <div class="headline-card" style="border-left-color:${a}">
      <div class="hl-tag" style="color:${a};border-color:${a}">${escapeHtml(h.tag)}</div>
      <div class="hl-meta">ERD&#337;S #${h.n}</div>
      <h3><a href="${h.href}">${escapeHtml(h.title)}</a></h3>
      <p class="summary">${escapeHtml(h.line)}</p>
      <a href="${h.href}" class="cta" style="border-color:${a};color:${a}">Read the report &#8599;</a>
    </div>`;
  }).join("\n");
  return `
<div class="section-header js-today"><h2>Headlines</h2><div class="line"></div></div>
<div class="headlines js-today">
${cards}
</div>`;
}

function homeHtml() {
  const rows = ledgerRows();
  const fullList = rows.map(ledgerItemHtml).join("\n");

  return layout({
    title: `${SITE} — Watch me vibe-math my way to discoveries`,
    description: "I'm a pretty regular dude. Every day my AI partner and I take on one of Paul Erdős's still-open problems, live. This is the complete, unedited record — every problem attempted, write-ups and working reports alike.",
    path: "/",
    body: `
<div class="hero">
  <span class="kicker">DAY ${dayNumber()} // THE VIBE-MATHING CHALLENGE</span>
  <h1 class="hero-h1">WATCH ME <span class="gold">VIBE-MATH</span> MY WAY TO DISCOVERIES.</h1>
  <p class="hero-sub">I'm Patrick — a pretty regular dude, not a mathematician. Every day, my
  AI partner and I pick one of Paul Erdős's still-unsolved problems and go after it, live.
  Some days we crack one. Most days we don't. No editing, no do-overs — this is the actual record.
  Below is the complete ledger: every problem we've touched, the full write-ups and the
  raw working reports alike.</p>
  <div class="hero-links">
    <a href="${VIBE_MATHING_URL}" target="_blank" rel="noopener">Read the full story ↗</a>
    <a href="${TWITTER_URL}" target="_blank" rel="noopener">Follow on X ↗</a>
  </div>
</div>

${ledgerScoreboard(rows)}

${headlinesHtml()}

<div class="section-header"><h2>The Record</h2><div class="line"></div></div>
<div class="filter-bar" id="filterBar" hidden><span id="filterBarText"></span><button type="button" id="filterClear">✕ show all</button></div>
<div class="record-list" id="recordList">
${fullList}
</div>

`,
  });
}

function entryHtml(e) {
  // Receipts (chatgpt.com transcripts of the AI exchanges) render as their own
  // gold-headed block — they ARE the verifiable proof-of-work, not just another
  // citation. Everything else (problem page, papers, our verification code) goes
  // under Sources. Adopted 2026-07-26; applies to every existing + future entry.
  const isReceipt = (u) => /chatgpt\.com\//.test(u);
  const linkBlock = (heading, cls, list) => list.length
    ? `<div class="links-list"><div class="links-heading ${cls}">${heading}</div>${list.map((l) => `<a href="${l.url}" target="_blank" rel="noopener">${escapeHtml(l.label)} ↗</a>`).join("\n")}</div>`
    : "";
  const linksHtml =
    linkBlock("Receipts — the raw AI exchanges", "lh-receipt", e.links.filter((l) => isReceipt(l.url))) +
    linkBlock("Sources & verification", "lh-source", e.links.filter((l) => !isReceipt(l.url)));
  const titleAlreadyHasNum = e.title.trim().startsWith(`#${e.problemNum}`);
  return layout({
    title: titleAlreadyHasNum
      ? `Erdős ${e.title} — ${SITE}`
      : `Erdős #${e.problemNum}: ${e.title} — ${SITE}`,
    description: e.summary,
    path: `/day/${e.slug}`,
    body: `
<article>
  <div class="problem-num">ERDŐS #${e.problemNum}</div>
  <h1>${escapeHtml(e.title)}</h1>
  <div class="meta-row">${statusBadge(e.status)}<span class="date">${formatDate(e.date).toUpperCase()}</span></div>
  <div class="body-content">${e.body}</div>
  ${linksHtml}
</article>
<p style="margin-top:2rem;font-family:'Rajdhani',sans-serif"><a href="/" style="font-weight:700;text-decoration:none">← back to the ledger</a></p>
`,
  });
}

function friendsHtml() {
  const sorted = [...friends].sort((a, b) => (a.date < b.date ? 1 : -1));
  const list = sorted.map((f) => `
    <div class="record-item">
      <div class="meta">${escapeHtml(f.kind)} · ${formatDate(f.date).toUpperCase()}</div>
      <h3>${escapeHtml(f.title)}</h3>
      <p class="summary">${escapeHtml(f.body)}</p>
      ${f.link ? `<a href="${f.link.url}" style="font-family:'Rajdhani',sans-serif;font-weight:700;text-decoration:none;color:var(--gold)">${escapeHtml(f.link.label)} →</a>` : ""}
    </div>
  `).join("\n");

  return layout({
    title: `Friends We Made Along The Way — ${SITE}`,
    description: "Secondary findings: lemmas that outlived a wrong conjecture, side quests picked up while scouting, literature we tripped over.",
    path: "/friends",
    body: `
<div class="hero" style="margin-bottom:1.5rem">
<span class="kicker">SECONDARY FINDINGS</span>
<h1 class="hero-h1" style="font-size:clamp(2rem,5.5vw,3.2rem)">FRIENDS WE MADE <span class="gold">ALONG THE WAY</span></h1>
<p class="hero-sub">Not every real result fits the daily format. Some days the actual target
gets refuted and something smaller but genuine survives the wreckage. Some days we're
scouting for tomorrow's problem and trip over a different one entirely. This is where
those live.</p>
</div>
<div class="record-list">
${list}
</div>
`,
  });
}

function scoutingHtml() {
  return layout({
    title: `How We Pick — ${SITE}`,
    description: "We reverse-engineered someone else's winning streak to find our own targets. Here's the actual analysis, not just the picks.",
    path: "/scouting",
    body: `
<div class="hero" style="margin-bottom:1.5rem">
<span class="kicker">HOW WE PICK</span>
<h1 class="hero-h1">WE REVERSE-ENGINEERED <span class="gold">SOMEONE ELSE'S WINNING STREAK.</span></h1>
<p class="hero-sub">Every problem on this site — #324, #677, #389 first, then #1109, #700, #1108, #931, #357, #1063 —
traces back to one scouting pass. This is that pass, close to verbatim. Not the polished
version, the actual working analysis.</p>
</div>

<div class="about-block">
<p>A few days before this site existed, Shouqiao Wang posted that he'd solved six open
Erdős problems in five days using the same model we use (GPT-5.6 Sol). Real pickup, real
skepticism too. Our question wasn't "is that legit" — it was: <strong>what actually made
those six problems fall, and can we find MORE problems shaped like that, on purpose,
instead of by luck?</strong></p>

<h2>What Wang's six wins actually looked like</h2>
<p>Not a tidy cluster. #390 (factorial as a product of larger integers) used smooth-number
asymptotics and a Poisson–Dickman calculation. #486 (avoiding prescribed residues) was a
pure explicit construction — synchronized deletion blocks at scale 2^j. #536 (equal
pairwise LCMs) reduced a multiplicative question into an additive-combinatorics forbidden
configuration and invoked a cap-set theorem. #788 used seeded extractors and
Trevisan–Raz–Reingold–Vadhan machinery. #1002 found a Cauchy limiting law hiding inside an
arithmetic sum. #1038 was mostly Tao's own prior reduction, finished with certified
interval arithmetic. Six completely different toolkits.</p>

<h2>The actual shared signature</h2>
<p>Not subject matter. Not difficulty level. Not "elementary." The real pattern:</p>
<p style="font-family:'Teko',sans-serif;font-size:1.6rem;color:var(--gold);text-transform:uppercase;letter-spacing:.5px">
Known hammer + nontrivial dictionary + auditable cleanup.</p>
<p>Every one of the six admits an alternate encoding — valuation vectors, finite-field
kernels, rational "shots," atomic root measures, synchronized residue blocks. Once
re-encoded, the target resembles an existing theorem or a finite optimization problem.
The proof decomposes into modules that can be attacked and audited separately.
Counterexamples to intermediate lemmas are cheap to generate. The edge wasn't inventing a
new field-level idea — it was finding the right representation, importing a known result,
and grinding through the awkward translation with repeated self-audit.</p>

<h2>What to look for — and what to avoid</h2>
<p><strong>Good signs:</strong> a single crisp existence/collision/asymptotic question · a
natural finite-dimensional encoding · a sibling theorem that already supplies most of the
machinery · a recent partial result isolating one explicit missing lemma · the hard step
being translation or lifting rather than a genuinely new phenomenon · a construction
testable on millions of small cases before generalizing.</p>
<p><strong>Bad signs:</strong> a famous conjecture with no visible reduction · a question
whose first plausible route needs new prime-distribution input · broad classification
problems with no canonical subproblem · finite data that looks structured but might just
reflect a deep Diophantine obstruction · several competing AI manuscripts already
circulating · ambiguous wording nobody's agreed on the meaning of.</p>

<h2>Where it pointed us</h2>
<p>Ranked by fit to that signature, not general importance — with our own live crowding
checks layered in (numbers below are the scout's own inference, unverified against the
forum until we actually picked each one up):</p>
<ol style="padding-left:1.3rem">
<li><a href="/day/324-sidon-polynomial">#324</a> — cleanest determinant-method surface, one
valid polynomial ends it, low crowding. <strong>Picked first.</strong></li>
<li><a href="/day/677-lcm-bridge">#677</a> — tailor-made for valuation-vector analysis,
resembles our own #477 work, nearly uncrowded. <strong>Picked second.</strong></li>
<li><a href="/day/389-shift-lemma-refuted">#389</a> — best explicit-construction gamble,
matches the iterative loop that worked on #477. <strong>Picked third.</strong></li>
<li><a href="/day/1109-squarefree-sumset">#1109</a> — squarefree sumset, modular pipeline,
low crowding.</li>
<li>#357 — distinct consecutive sums, a Golomb-ruler/Sidon dictionary, real prior
literature to respect.</li>
<li>#700 — gcd(n, C(n,k)), a Kummer's-theorem carry-counting encoding, very quiet.</li>
<li>#931 and #1108 — named but not yet picked up; #931's crowding was rising even at
scout time (an active partial result on the (4,3) case), #1108 carries a literature-status
flag worth resolving before attempting.</li>
</ol>
<p>Explicitly excluded: #689 and #421, both already crowded with competing AI attempts —
not our shape of edge.</p>

<h2>The honest caveat</h2>
<p>Every probability estimate in the original scouting pass was labeled, plainly,
"inference, not sourced" — a relative gut-check on tractability, not a calibrated number.
We treat it that way here too. This page is a methodology artifact, not a results page —
the actual verified outcomes live on <a href="/">the log</a>.</p>
</div>
`,
  });
}

function aboutHtml() {
  const defs = [
    { badge: `<span class="tag-writeup">ATTEMPTED</span>`, text: "Every numbered problem we've taken a real run at — full write-ups and raw working reports alike. The denominator everything else on the board sits under." },
    { badge: `<span class="badge badge-closed">CLOSED</span>`, text: "The problem is closed — a real proof exists, and we checked it independently against primary sources, by hand, or by computation. Includes closes by others that we verified. Most are not yet posted at erdosproblems.com — their bar is a human proof-check or Lean, and we hold ourselves to it before claiming anything there." },
    { badge: `<span class="badge badge-closed">CLOSED BY US</span>`, text: "Closed, and the proof originated with us — not just verified by us. (#477: the Erdős–Graham conjecture, for every K≥3.)" },
    { badge: `<span class="badge badge-partial">VERIFIED PARTIAL</span>`, text: "A real sub-result landed and we verified it — a reformulation, a pinned special case, a new bound — but the full problem stays open. Also home to the decisive checks (PROVED / FOUND badges): the times a statement as literally printed turned out to be false or ill-posed, usually already noted in the tracker's own forum, which we then independently certify. A genuine piece of the answer, not a consolation prize." },
    { badge: `<span class="badge badge-live">LIVE</span>`, text: "Brief's out to a second reasoning model, or we're iterating rounds on it. No verdict yet." },
    { badge: `<span class="badge badge-noproof">WALL</span>`, text: "Nothing verified landed. Includes runs we never really started — a live worker or a claimed proof was already on the problem page, so our no-collision rule fired (those rows wear a SKIPPED badge; we stopped out of respect, not out of steam). Attempted is attempted — the honest record shows all of it." },
  ].map((d) => `<div class="status-def">${d.badge}<div>${d.text}</div></div>`).join("\n");

  return layout({
    title: `About — ${SITE}`,
    description: "The pitch, the process, and the one honest hedge we allow ourselves.",
    path: "/about",
    body: `
<div class="hero" style="margin-bottom:1.5rem">
<span class="kicker">THE PITCH</span>
<h1 class="hero-h1" style="font-size:clamp(2rem,5vw,2.8rem)">I'M A PRETTY REGULAR DUDE WITH AN AI PARTNER. THIS IS WHAT WE'RE TESTING.</h1>
</div>
<div class="about-block">
<p>Watch <a href="${VIBE_MATHING_URL}" target="_blank" rel="noopener">what happened when I started vibe-mathing</a> —
that's the longer story. This site is the daily version of it: one open Erdős problem,
every day, live, no editing.</p>

<div class="section-header"><h2>The Process</h2><div class="line"></div></div>
<p>We pull candidates from <a href="${CREDIT_URL}" target="_blank" rel="noopener">T. F. Bloom's erdosproblems.com</a>
— full credit, we're not building a competing list. We hunt for problems that are genuinely
tractable but neglected, run our own computation on them before writing anything (small-N
searches, known-witness checks, sanity checks), then send a sharp brief to a second,
independent reasoning model (currently GPT-5.6 Sol via ChatGPT Pro). Whatever comes back
gets independently checked — against primary sources, by hand, or by fresh computation —
before we call it anything.</p>

<div class="section-header"><h2>The Scoreboard, Decoded</h2><div class="line"></div></div>
${defs}
<p style="margin-top:1.2rem">Each row also wears its own badge, finer than the boxes:
<strong style="color:var(--text-bright)">FULL WRITE-UP</strong> — a complete entry with its own page ·
<strong style="color:var(--text-bright)">PROVED / FOUND</strong> — a decisive verified check, often that the printed statement is false (we certify; we don't claim priority) ·
<strong style="color:var(--text-bright)">SKIPPED</strong> — the no-collision rule fired before we started ·
<strong style="color:var(--text-bright)">NO PROGRESS</strong> — probed, nothing to show as ours.</p>

<div class="section-header"><h2>Disclosure</h2><div class="line"></div></div>
<p>Plainly AI-assisted. Claude does real verification work here, not ghostwriting — GPT-5.6 Sol
does the independent attempt, I relay and make the calls on what gets published. Every entry
says exactly what happened.</p>
</div>
`,
  });
}

// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
let _mdStash = [];
function mdToHtml(md) {
  _mdStash = [];
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));
  const stash = (s) => { _mdStash.push(s); return "@@S" + (_mdStash.length - 1) + "@@"; };
  md = md.replace(/```[^\n]*\n?([\s\S]*?)```/g, (m, code) => stash("<pre><code>" + esc(code) + "</code></pre>"));
  // Escape &,<,> inside math so a stray `<` (e.g. M<p) can't open a phantom tag
  // in the HTML text node before KaTeX runs; auto-render reads decoded textContent.
  const mesc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  md = md.replace(/\\\[[\s\S]*?\\\]/g, (m) => stash(mesc(m)));
  md = md.replace(/\$\$[\s\S]*?\$\$/g, (m) => stash(mesc(m)));
  md = md.replace(/\\\([\s\S]*?\\\)/g, (m) => stash(mesc(m)));
  md = md.replace(/`([^`\n]+)`/g, (m, c) => stash("<code>" + esc(c) + "</code>"));
  const inline = (s) => {
    s = esc(s);
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>");
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, "<a href=\"$2\">$1</a>");
    return s;
  };
  const out = [];
  let para = [];
  let listType = null;
  let listItems = [];
  let inBq = false;
  let bqBuf = [];
  const isDisp = (i) => { const s = _mdStash[+i]; return !!s && (s.indexOf("\\[") === 0 || s.indexOf("$$") === 0); };
  const flushPara = () => { if (para.length) { out.push("<p>" + inline(para.join(" ")) + "</p>"); para = []; } };
  const flushList = () => { if (listType) { out.push("<" + listType + ">" + listItems.join("") + "</" + listType + ">"); listType = null; listItems = []; } };
  const flushBq = () => { if (!inBq) return; let runs = [], h2 = ""; const emit = () => { if (runs.length) { h2 += "<p>" + inline(runs.join(" ")) + "</p>"; runs = []; } }; for (const l of bqBuf) { if (l === "") emit(); else runs.push(l); } emit(); out.push("<blockquote>" + h2 + "</blockquote>"); inBq = false; bqBuf = []; };
  const flushAll = () => { flushPara(); flushList(); flushBq(); };
  for (const raw of md.split("\n")) {
    const line = raw.replace(/\s+$/, "");
    if (/^\s*$/.test(line)) { flushAll(); continue; }
    const ph = line.match(/^@@S(\d+)@@$/);          // a stashed block on its own line
    if (ph) {
      flushAll();
      out.push(isDisp(ph[1]) ? ("<div class=\"math-block\">@@S" + ph[1] + "@@</div>") : ("<p>@@S" + ph[1] + "@@</p>"));
      continue;
    }
    const bq = line.match(/^>\s?(.*)$/);            // markdown blockquote line (math inside stays stashed)
    if (bq) { flushPara(); flushList(); inBq = true; bqBuf.push(bq[1]); continue; }
    if (inBq) flushBq();
    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) { flushAll(); const lv = Math.min(h[1].length + 1, 6); out.push("<h" + lv + ">" + inline(h[2]) + "</h" + lv + ">"); continue; }
    const ol = line.match(/^\s*\d+\.\s+(.*)$/);
    const ul = line.match(/^\s*[-*+]\s+(.*)$/);
    if (ol) { if (listType !== "ol") { flushPara(); flushList(); listType = "ol"; } listItems.push("<li>" + inline(ol[1]) + "</li>"); continue; }
    if (ul) { if (listType !== "ul") { flushPara(); flushList(); listType = "ul"; } listItems.push("<li>" + inline(ul[1]) + "</li>"); continue; }
    flushList();
    para.push(line);                                  // soft-wrapped lines join into one paragraph
  }
  flushAll();
  let html = out.join("\n");
  html = html.replace(/@@S(\d+)@@/g, (m, i) => _mdStash[+i]);
  return html;
}

function reportHtml(n) {
  const r = LEDGER.find((x) => x.n === n);
  if (!r) return null;
  const map = { PROVED:{c:"closed",l:"PROVED"}, FOUND:{c:"closed",l:"FOUND"}, PARTIAL:{c:"confirmed",l:"PARTIAL"}, WALL:{c:"noproof",l:"WALL"}, SKIP:{c:"noproof",l:"SKIPPED"} };
  const b = map[r.verdict] || { c:"noproof", l:r.verdict };
  return layout({
    title: "Erdoes #" + r.n + " - working report - " + SITE,
    description: r.gist,
    path: "/report/" + r.n,
    body: `
<p class="meta" style="margin-bottom:1rem"><a href="/" style="font-weight:700">&larr; back to the ledger</a></p>
<div class="meta">ERD&#337;S #${r.n} &middot; <span class="badge badge-${b.c}">${b.l}</span></div>
<article class="body-content" style="margin-top:1rem">${mdToHtml(r.md)}</article>
<p class="meta" style="margin-top:2rem">This is the AI working report, labelled by outcome &mdash; not an
independently verified claim unless marked PROVED. <a href="/">&larr; ledger</a></p>
`,
  });
}

function sitemapXml() {
  const rows = ledgerRows();
  const newest = (rows[0] && rows[0].date) || LAUNCH_DATE;
  const urls = [
    { loc: "/", lastmod: newest },
    { loc: "/friends", lastmod: newest },
    { loc: "/scouting", lastmod: newest },
    { loc: "/about", lastmod: newest },
    ...entries.map((e) => ({ loc: `/day/${e.slug}`, lastmod: e.date })),
    ...LEDGER.map((r) => ({ loc: `/report/${r.n}`, lastmod: r.d || "" })),
  ].filter((u) => u.lastmod);
  const body = urls
    .map((u) => `  <url><loc>https://erdosproblemaday.com${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>`)
    .join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    let path = url.pathname.replace(/\/+$/, "") || "/";

    if (path === "/robots.txt") {
      return new Response("User-agent: *\nAllow: /\nSitemap: https://erdosproblemaday.com/sitemap.xml\n", {
        headers: { "content-type": "text/plain" },
      });
    }
    if (path === "/sitemap.xml") {
      return new Response(sitemapXml(), { headers: { "content-type": "application/xml" } });
    }
    if (path === "/favicon.svg") {
      return new Response(FAVICON_SVG, { headers: { "content-type": "image/svg+xml", "cache-control": "public, max-age=86400" } });
    }
    if (path === "/og-image.jpg") {
      return new Response(base64ToBytes(OG_IMAGE_B64), { headers: { "content-type": "image/jpeg", "cache-control": "public, max-age=86400" } });
    }
    if (path === "/") {
      return new Response(homeHtml(), { headers: { "content-type": "text/html;charset=UTF-8" } });
    }
    if (path === "/about") {
      return new Response(aboutHtml(), { headers: { "content-type": "text/html;charset=UTF-8" } });
    }
    if (path === "/scouting") {
      return new Response(scoutingHtml(), { headers: { "content-type": "text/html;charset=UTF-8" } });
    }
    if (path === "/progress") {
      // The ledger IS the homepage now; keep the old URL alive for bookmarks.
      return new Response(null, { status: 301, headers: { location: "/" } });
    }
    if (path === "/friends") {
      return new Response(friendsHtml(), { headers: { "content-type": "text/html;charset=UTF-8" } });
    }
    const m = path.match(/^\/day\/([a-z0-9-]+)$/);
    if (m) {
      const e = entries.find((x) => x.slug === m[1]);
      if (e) return new Response(entryHtml(e), { headers: { "content-type": "text/html;charset=UTF-8" } });
    }
        {
      const rm = path.match(/^\/report\/(\d+)$/);
      if (rm) {
        const h = reportHtml(parseInt(rm[1], 10));
        if (h) return new Response(h, { headers: { "content-type": "text/html;charset=UTF-8" } });
      }
    }
return new Response("Not found", { status: 404 });
  },
};
